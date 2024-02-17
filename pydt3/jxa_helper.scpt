JsOsaDAS1.001.00bplist00ÑVscript_,,class ObjectPoolManager {
    constructor() {
        this._currentId = 0;
        this._objectIdMap = new Map();
        this._idObjectMap = new Map();
    }

    getObject(id) {
        try {
            return this._idObjectMap.get(id);
        } catch (error) {
            console.log(`Error getting object with id: ${id}`);
        }
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
    static getAssociatedApplicationName(obj) {
        let displayString = Automation.getDisplayString(obj);
        let m = displayString.match(/^Application\(['"]([^)]*)['"]\)/);
        if (m) {
            let name = m[1];
            return name;
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
        let classOf = ObjectSpecifier.classOf(specifier);
        if (classOf === 'application') {
            return 'application';
        }
        if (this.guessIsSpecifierContainer(specifier)) {
            return 'array::' + classOf;
        }
        if (specifier.class !== undefined) {
            try {
                specifierClass = specifier.class();
            } catch (e) {
                if (e.errorNumber === -1700) {
                    // The object is not a specifier.
                    return classOf;
                }
            }
            return specifierClass;
        }
        return classOf;
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

        if (ObjectSpecifier.hasInstance(obj)) {
            let guessClass = Util.guessClassOfSpecifier(obj);
            if (guessClass === undefined) {
                return {
                    type: 'reference',
                    objId: this.objectPoolManager.getId(obj),
                    app: Util.getAssociatedApplicationName(obj),
                    className: 'unknown'
                }
                // We don't do implicit evaluation of specifiers anymore.
                
                // The object is a specifier but we don't know its class.
                // This could mean that the object is a reference to a primitive value.
                // eg. a `number`, `bool` or `string`.
                // In that case, the best we can do is to return the evaluated value.
                // try {
                //     let evaluated = obj();
                //     if (Util.isJsonNode(evaluated)) {
                //         return {
                //             type: 'plain',
                //             data: evaluated
                //         };
                //     } else if (evaluated instanceof Date) {
                //         return {
                //             type: 'date',
                //             data: evaluated.getTime() / 1000
                //         }
                //     } else {
                //         return {
                //             type: 'reference',
                //             objId: this.objectPoolManager.getId(obj),
                //             app: Util.getAssociatedApplicationName(obj),
                //             className: 'unknown'
                //         }
                //     }
                // } catch (error) {
                //     return {
                //         type: 'reference',
                //         objId: this.objectPoolManager.getId(obj),
                //         app: Util.getAssociatedApplicationName(obj),
                //         className: 'unknown'
                //     }
                // }
            }

            if (guessClass === 'application') {
                return {
                    type: 'reference',
                    objId: this.objectPoolManager.getId(obj),
                    app: Util.getAssociatedApplicationName(obj),
                    className: 'application'
                }
            }

            if (guessClass.startsWith('array::')) {
                return {
                    type: 'reference',
                    objId: this.objectPoolManager.getId(obj),
                    app: Util.getAssociatedApplicationName(obj),
                    className: guessClass
                }
            }

            return {
                type: 'reference',
                objId: this.objectPoolManager.getId(obj),
                className: guessClass,
                app: Util.getAssociatedApplicationName(obj),
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
            try {
                return this.objectPoolManager.getObject(obj.objId);
            } catch (error) {
                console.log(`Error unwrapping object with id: ${obj.objId}`);
            }
        }
    }

    strIOFuncWrapper(func) {
        return  (strParams) => {
            let params = JSON.parse(strParams);
            try {
                params = this.unwrapFromJson(params);
            } catch (error) {
                console.log(`Error unwrapping params: ${error}`);
            }
            let result = func(params);
            try {
                result = this.wrapToJson(result);
            } catch (error) {
                console.log(`Error wrapping result: ${error}`);
            }
            return JSON.stringify(result);
        }
    }
}



const objectPoolManager = new ObjectPoolManager();
const jsonTranslator = new JsonTranslator(objectPoolManager);


function _echo(params) {
    return params;
}
echo = jsonTranslator.strIOFuncWrapper(_echo);

function _releaseObjectWithId({id}) {
    objectPoolManager.releaseObjectWithId(id);
}
releaseObjectWithId = jsonTranslator.strIOFuncWrapper(_releaseObjectWithId);

function _getApplication({name}) {
    // throw new Error(`Application name: ${name} not found, typeof name: ${typeof name}`);
    let theApp = Application(name);
    theApp.includeStandardAdditions = true
    return theApp;
}
getApplication = jsonTranslator.strIOFuncWrapper(_getApplication);

function _evalJXACodeSnippet({source, locals}) {
    for (let k in locals) {
        eval(`var ${k} = locals[k];`);
    }
    const value = eval(source);
    return value;
}
evalJXACodeSnippet = jsonTranslator.strIOFuncWrapper(_evalJXACodeSnippet);

function _evalAppleScriptCodeSnippet({source}) {
    let app = Application.currentApplication();
    app.includeStandardAdditions = true;

    let result = app.runScript(source, {in: 'AppleScript'});
    return result;
}
evalAppleScriptCodeSnippet = jsonTranslator.strIOFuncWrapper(_evalAppleScriptCodeSnippet);

function _getProperty({obj, name}) {
    let value = obj[name];
    if (Util.isMethod(value)) {
        value = value.bind(obj);
    }
    return value;
}
getProperty = jsonTranslator.strIOFuncWrapper(_getProperty);

function _getProperties({obj, properties}) {
    let result = {};
    for (let k of properties) {
        result[k] = _getProperty({obj, name: k});
    }
    return result;
}
getProperties = jsonTranslator.strIOFuncWrapper(_getProperties);

function _setProperties({obj, keyValues}) {
    for (let k in keyValues) {
        obj[k] = keyValues[k];
    }
}
setProperties = jsonTranslator.strIOFuncWrapper(_setProperties);

function _callMethod({obj, name, args, kwargs}) {
    let method = obj[name];
    if (method === undefined) {
        throw new Error(`Method not found: ${name}`);
    }
    if (Util.isMethod(method)) {
        method = method.bind(obj);

    }
    if (args === null || args === undefined) {
        args = [];
    }

    if (kwargs === null || kwargs === undefined) {
        return method(...args);
    } else {
        return method(...args, kwargs);
    }
}
callMethod = jsonTranslator.strIOFuncWrapper(_callMethod);

function _callSelf({obj, args, kwargs}) {
    return obj(...args, kwargs);
}
callSelf = jsonTranslator.strIOFuncWrapper(_callSelf);                              ,Bjscr  úÞÞ­