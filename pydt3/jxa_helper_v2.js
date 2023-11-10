class ObjectPoolManager {
    constructor() {
        this._currentId = 0;
        this._obj = {};
        this._objectIdMap = new WeakMap();
    }
    getObject(id) {
        return this._pool[id];
    }

    getId(obj) {
        if (!this._objIdMap.has(obj)) {
            this.currentId += 1;
            map.set(object, this.currentId);
        }
        return map.get(object);
    }

    releaseObjectWithId(objectId) {
        delete objectCacheMap[objectId];
    }
}

class Util {
    static getAssociatedApplication(obj) {
        let displayString = Automation.getDisplayString(obj);
        let m = displayString.match(/^Application\(['"]([^)]*)['"]\)/);
        if (m) {
            return Application(name);
        }
        return null;
    }

    static guessIsSpecifierContainer(specifier) {
        if (!ObjectSpecifier.hasInstance(specifier)) {
            return false;
        }
        let proto = Object.getPrototypeOf(specifier);
        const testPropNames = ['whose', 'at'];
        return testPropNames.every((propName) => propName in proto);
    }

    static guessClassOfSpecifier(specifier) {
        // It's at best a guess due to the nature of JXA.
        if (!ObjectSpecifier.hasInstance(specifier)) {
            return undefined;
        }
        let specifierClass = undefined;
        if (this.guessIsSpecifierContainer(specifier)) {
            specifierClass = ObjectSpecifier.classOf(specifier);
            return 'array::' + specifierClass;
        }
        try {
            specifierClass = specifier.class();
        } catch (e) {
            if (e.errorNumber === -1700) {
                // The object is not a specifier.
                return undefined;
            }
        }

        return specifierClass;
    }

    static isJsonNode(obj) {
        return obj === null || ['undefined', 'string', 'number', 'boolean'].includes(typeof obj);
    }

    static isPlainJson(obj) {
        if (this.isJsonNode(obj)) {
            return true;
        } else if (typeof obj === 'object') {
            for (let k in obj) {
                if (!this.isJsonNode(obj[k])) {
                    return false;
                }
            }
            return true;
        } else if (typeof obj === 'function') {
            return false;
        }
    }

    static isMethod(obj) {
        return typeof obj === 'function' && obj.constructor.name === 'Function';
    }
}

class JsonTranslator {
    /**
     * @param {ObjectPoolManager} objectPoolManager 
     */
    constructor(objectPoolManager) {
        this.objectPoolManager = objectPoolManager;
    }

    wrapToJson(obj) {
        if (obj === undefined) {
            obj = null;
        }

        if (Util.isJsonNode(obj)) {
            return {
                type: 'plain',
                data: obj
            }
        }

        if (typeof obj === 'object') {
            // TODO: Handle Date
            if (obj instanceof Date) {
                return {
                    type: 'date',
                    data: obj.getTime() / 1000
                }
            }
            if (Array.isArray(obj)) {
                let data = []
                for (let i in obj) {
                    data[i] = this.wrapToJson(obj[i]);
                }
                return {
                    type: 'array',
                    data: data
                }
            }
            if (obj.constructor.name === 'Object') {
                let data = {}
                for (let k in obj) {
                    data[k] = this.wrapToJson(obj[k]);
                }
                return {
                    type: 'dict',
                    data: data
                }
            }

            throw new Error(`wrapObjToJson: Unknown type: ${typeof obj}`);
        }

        if (ObjectSpecifier.hasInstance(obj)) {
            let guessClass = Util.guessClassOfSpecifier(obj);
            if (guessClass === undefined) {
                // The object is a specifier but we don't know its class.
                // This could mean that the object is a reference to a primitive value.
                // eg. a `number`, `bool` or `string`.
                // In that case, the best we can do is to return the evaluated value.
                let evaluated = obj();
                return this.wrapToJson(evaluated);
            }

            if (guessClass === 'application') {
                return {
                    type: 'reference',
                    objId: this.objectPoolManager.getId(obj),
                    plainRepr: null,
                    className: 'application'
                }
            }

            if (guessClass.startsWith('array::')) {
                return {
                    type: 'reference',
                    objId: this.objectPoolManager.getId(obj),
                    plainRepr: null,
                    className: guessClass
                }
            }

            // If the evaluated object is a plain object, return the evaluated value.
            // WARNING: This may cause problems if the object is a reference to a text or dict.
            //          In that case, the object "can" be interpreted as a plain object but still
            //          has properties that are references to other objects.
            let evaluated = obj();
            if (!Util.isPlainJson(evaluated)) {
                evaluated = null;
            }

            return {
                type: 'reference',
                objId: this.objectPoolManager.getId(obj),
                className: guessClass,
                plainRepr: evaluated
            }
        }

        if (typeof obj === 'function') {
            return {
                type: 'reference',
                objId: this.objectPoolManager.getId(obj)(obj),
                className: 'function'
            }
        }

        throw new Error(`Unknown type: ${typeof obj}`);
    }

    unwrapFromJson(obj) {
        if (obj.type === 'plain') {
            return obj.data;
        } else if (obj.type === 'date') {
            return new Date(obj.data * 1000);
        } else if (obj.type === 'array' || obj.type === 'dict') {
            for (let k in obj.data) {
                obj.data[k] = this.unwrapFromJson(obj.data[k]);
            }
            return obj.data;
        } else if (obj.type === 'reference') {
            return this.objectPoolManager.getObject(obj.objId);
        }
    }
}

class ExternalCallHelper {
    /**
     * 
     * @param {ObjectPoolManager} objectPoolManager 
     * @param {JsonTranslator} jsonTranslator 
     */
    constructor(objectPoolManager, jsonTranslator) {
        this.objectPoolManager = objectPoolManager;
        this.jsonTranslator = jsonTranslator;
    }

    externalCall(inputString) {
        const inputJson = JSON.parse(inputString);
        const params = this.jsonTranslator.unwrapFromJson(inputJson);
        const result = this.callMethod(params);
        const outputJson = this.jsonTranslator.wrapToJson(result);
        return JSON.stringify(outputJson);
    }

    callMethod({name, params}) {
        Exports[name](params);
    }
}

class Exports {
    static releaseObjectWithId({id}) {
        objectPoolManager.releaseObjectWithId(id);
    }

    static getApplication({name}) {
        let app = Application(name);
        app.includeStandardAdditions = true
        return app;
    }

    static evalJXACodeSnippet({source, locals}) {
        for (let k in locals) {
            eval(`var ${k} = locals[k];`);
        }
        return eval(source);
    }

    static evalAppleScriptCodeSnippet({source}) {
        let app = Application.currentApplication();
        app.includeStandardAdditions = true;

        let result = app.runScript(source, {in: 'AppleScript'});
        return result;
    }

    static getProperties({object, properties}) {
        let result = {};
        for (let k of properties) {
            result[k] = object[k];
            if (Util.isMethod(result[k])) {
                result[k] = result[k].bind(object);
            }
        }
        return result;
    }

    static setProperties({object, keyValues}) {
        for (let k in keyValues) {
            object[k] = keyValues[k];
        }
    }

    static callMethod({object, name, args}) {
        let method = object[name];
        if (method === undefined) {
            throw new Error(`Method not found: ${name}`);
        }
        return this.callSelf({object: method, args});
    }

    static callSelf({object, args}) {
        object(...args);
    }
    
}

const objectPoolManager = new ObjectPoolManager();
const jsonTranslator = new JsonTranslator(objectPoolManager);
const externalCallHelper = new ExternalCallHelper(objectPoolManager, jsonTranslator);


function externalCall(inputString) {
    externalCallHelper.externalCall(inputString);
}