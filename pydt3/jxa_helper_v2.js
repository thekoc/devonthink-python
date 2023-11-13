class ObjectPoolManager {
    constructor() {
        this._currentId = 0;
        this._objectIdMap = new Map();
        this._idObjectMap = new Map();
    }

    getObject(id) {
        return this._idObjectMap.get(id);
    }

    getId(obj) {
        if (!this._objectIdMap.has(obj)) {
            this._currentId += 1;
            this._objectIdMap.set(obj, this._currentId);
            this._idObjectMap.set(this._currentId, obj);
        }
        return this._currentId;
    }

    releaseObjectWithId(objectId) {
        const obj = this.getObject(objectId);
        this._idObjectMap.delete(objectId);
        this._objectIdMap.delete(obj);
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
        // If it is an array specifier.
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
                objId: this.objectPoolManager.getId(obj),
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

    strIOFuncWrapper(func) {
        return  (strParams) => {
            let params = JSON.parse(strParams);
            params = this.unwrapFromJson(params);
            let result = func(params);
            result = this.wrapToJson(result);
            return JSON.stringify(result);
        }
    }
}



const objectPoolManager = new ObjectPoolManager();
const jsonTranslator = new JsonTranslator(objectPoolManager);


// const echo = jsonTranslator.strIOFuncWrapper((params) => {
//     return params;
// });

function echo(params) {
    return params;
}
echo = jsonTranslator.strIOFuncWrapper(echo);



function releaseObjectWithId({id}) {
    objectPoolManager.releaseObjectWithId(id);
}
releaseObjectWithId = jsonTranslator.strIOFuncWrapper(releaseObjectWithId);

function getApplication({name}) {
    let app = Application(name);
    app.includeStandardAdditions = true
    return app;
}
getApplication = jsonTranslator.strIOFuncWrapper(getApplication);

function evalJXACodeSnippet({source, locals}) {
    for (let k in locals) {
        eval(`var ${k} = locals[k];`);
    }
    const value = eval(source);
    return {
        'string': JSON.stringify(value)
    }
}
evalJXACodeSnippet = jsonTranslator.strIOFuncWrapper(evalJXACodeSnippet);

function evalAppleScriptCodeSnippet({source}) {
    let app = Application.currentApplication();
    app.includeStandardAdditions = true;

    let result = app.runScript(source, {in: 'AppleScript'});
    return result;
}
evalAppleScriptCodeSnippet = jsonTranslator.strIOFuncWrapper(evalAppleScriptCodeSnippet);

function getProperties({obj, properties}) {
    let result = {};
    for (let k of properties) {
        result[k] = obj[k];
        if (Util.isMethod(result[k])) {
            result[k] = result[k].bind(obj);
        }
    }
    return result;
}
getProperties = jsonTranslator.strIOFuncWrapper(getProperties);

function setProperties({obj, keyValues}) {
    for (let k in keyValues) {
        obj[k] = keyValues[k];
    }
}
setProperties = jsonTranslator.strIOFuncWrapper(setProperties);

function callMethod({obj, name, args, kwargs}) {
    let method = obj[name];
    if (method === undefined) {
        throw new Error(`Method not found: ${name}`);
    }
    method = method.bind(obj);
    return method(...args, kwargs);
}
callMethod = jsonTranslator.strIOFuncWrapper(callMethod);

function callSelf({obj, args, kwargs}) {
    return obj(...args, kwargs);
}
callSelf = jsonTranslator.strIOFuncWrapper(callSelf);