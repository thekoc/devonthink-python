JsOsaDAS1.001.00bplist00ÑVscript_÷const getObjectId = (() => {
    let count = 0;
    const objIdMap = new WeakMap();
    return (object) => {
      const objectId = objIdMap.get(object);
      if (objectId === undefined) {
        count += 1;
        objIdMap.set(object, count);
        return count;
      }
    
      return objectId;
    }
})();


const objectCacheMap = {};

function cacheObjct(obj) {
    let id = getObjectId(obj);
    objectCacheMap[id] = obj;
    return id;
}

function getCachedObject(id) {
    return objectCacheMap[id];
}

function jsonIOWrapper(func) {
    return (param_str) => {
        let param = JSON.parse(param_str);
        let result = func(param);
        return JSON.stringify(result);
    }
}

const getAssociatedApplication = (() => {
    const appCache = {};
    return function getAssociatedApplication(obj) {
        let displayString = Automation.getDisplayString(window);
        let m = displayString.match(/^Application\(['"]([^)]*)['"]\)/);
        if (m) {
            let name = m[1];
            if (appCache[name] === undefined) {
                appCache[name] = Application(name);
            }
            return appCache[name];
        }
        return null;
    }
})();

function guessIsContainerSpecifier(specifier) {
    if (!ObjectSpecifier.hasInstance(specifier)) {
        return false;
    }
    let proto = Object.getPrototypeOf(specifier);
    const testPropNames = ['whose', 'at'];
    return testPropNames.every((propName) => propName in proto);
}

function guessClassOfSpecifier(specifier) {
    // It's at best a guess due to the nature of JXA.
    if (!ObjectSpecifier.hasInstance(specifier)) {
        return undefined;
    }
    let specifierClass = undefined;
    if (guessIsContainerSpecifier(specifier)) {
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

function isJsonNodeValue(obj) {
    return obj === null || ['undefined', 'string', 'number', 'boolean'].includes(typeof obj);
}

function isPlainObj(obj) {
    if (isJsonNodeValue(obj)) {
        return true;
    } else if (typeof obj === 'object') {
        for (let k in obj) {
            if (!isJsonNodeValue(obj[k])) {
                return false;
            }
        }
        return true;
    } else if (typeof obj === 'function') {
        return false;
    }
}


function wrapObjToJson(obj) {
    if (obj === undefined) {
        obj = null;
    }
    if (isJsonNodeValue(obj)) {
        return {
            type: 'plain',
            data: obj
        }
    }

    if (typeof obj === 'object') {
        // TODO: Handle Date
        if (obj instanceof Date) {
            return {
                type: 'plain',
                data: obj.toISOString()
            }
        }
        if (Array.isArray(obj)) {
            let data = []
            for (let i in obj) {
                data[i] = wrapObjToJson(obj[i]);
            }
            return {
                type: 'array',
                data: data
            }
        }
        if (obj.constructor.name === 'Object') {
            let data = {}
            for (let k in obj) {
                data[k] = wrapObjToJson(obj[k]);
            }
            return {
                type: 'dict',
                data: data
            }
        }

        throw new Error(`wrapObjToJson: Unknown type: ${typeof obj}`);
    }

    if (ObjectSpecifier.hasInstance(obj)) {
        let guessClass = guessClassOfSpecifier(obj);
        if (guessClass === undefined) {
            // The object is a specifier but we don't know its class.
            // This could mean that the object is a reference to a primitive value.
            // eg. a `number`, `bool` or `string`.
            // In that case, the best we can do is to return the evaluated value.
            let evaluated = obj();
            return wrapObjToJson(evaluated);
        }

        if (guessClass === 'application') {
            return {
                type: 'reference',
                objId: cacheObjct(obj),
                plainRepr: null,
                className: 'application'
            }
        }

        if (guessClass.startsWith('array::')) {
            return {
                type: 'reference',
                objId: cacheObjct(obj),
                plainRepr: null,
                className: guessClass
            }
        }

        // If the evaluated object is a plain object, return the evaluated value.
        // WARNING: This may cause problems if the object is a reference to a text or dict.
        //          In that case, the object "can" be interpreted as a plain object but still
        //          has properties that are references to other objects.
        let evaluated = obj();
        if (!isPlainObj(evaluated)) {
            evaluated = null;
        }

        return {
            type: 'reference',
            objId: cacheObjct(obj),
            className: guessClass,
            plainRepr: evaluated
        }
    }

    if (typeof obj === 'function') {
        return {
            type: 'reference',
            objId: cacheObjct(obj),
            className: 'function'
        }
    }

    throw new Error(`Unknown type: ${typeof obj}`);
}

function unwrapObjFromJson(obj) {
    if (obj.type === 'plain') {
        return obj.data;
    } else if (obj.type === 'array' || obj.type === 'dict') {
        for (let k in obj.data) {
            obj.data[k] = unwrapObjFromJson(obj.data[k]);
        }
        return obj.data;
    } else if (obj.type === 'reference') {
        return getCachedObject(obj.objId);
    }
}

function getApplication(params) {
    let name = params.name;
    let app = Application(name);
    app.includeStandardAdditions = true
    return wrapObjToJson(app);
}
getApplication = jsonIOWrapper(getApplication);

function isMethod(obj) {
    return typeof obj === 'function' && obj.constructor.name === 'Function';
}

function getProperties(params) {
    let objId = params.objId;
    let names = params.names;
    let obj = objectCacheMap[objId];
    let data = {};
    for (let n of names) {
        let property = obj[n];
        if (isMethod(property)) {
            property = property.bind(obj);
        }
        data[n] = wrapObjToJson(property);
    }
    return data;
}
getProperties = jsonIOWrapper(getProperties);


function setPropertyValues(params) {
    let objId = params.objId;
    let properties = params.properties;

    let obj = objectCacheMap[objId];

    for (let n in properties) {
        let value = properties[n];
        obj[n] = value;
    }
    return {};
}
setPropertyValues = jsonIOWrapper(setPropertyValues);

function callMethod(params) {
    let objId = params.objId;
    let name = params.name;
    let args = params.args;
    let kwargs = params.kwargs;

    let obj = getCachedObject(objId);
    let func;

    if (name === null) {
        func = obj
    } else {
        func = obj[name].bind(obj);
    }

    if (args === null) {
        args = [];
    }

    for (let i = 0; i < args.length; i++) {
        args[i] = unwrapObjFromJson(args[i]);
    }
    if (kwargs !== null) {
        for (let k in params.kwargs) {
            kwargs[k] = unwrapObjFromJson(params.kwargs[k]);
        }
    }

    let result = func(...args, kwargs);
    return wrapObjToJson(result);
}
callMethod = jsonIOWrapper(callMethod);


function releaseObject(params) {
    let objId = params.objId;
    delete objectCacheMap[objId];
    return {};
}
releaseObject = jsonIOWrapper(releaseObject);

function callSelf(params) {
    let objId = params.objId;
    let args = params.args;
    
    for (let i = 0; i < args.length; i++) {
        args[i] = unwrapObjFromJson(args[i]);
    }
    let kwargs = {};
    for (let k in params.kwargs) {
        kwargs[k] = unwrapObjFromJson(params.kwargs[k]);
    }
    let obj = objectCacheMap[objId];
    let result = obj(...args, kwargs);
    return wrapObjToJson(result);
}
callSelf = jsonIOWrapper(callSelf);                                jscr  úÞÞ­