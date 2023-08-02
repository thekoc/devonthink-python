const getObjectId = (() => {
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

    if (isJsonNodeValue(obj)) {
        return {
            type: 'plain',
            data: obj
        }
    }

    if (typeof obj === 'object') {
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
                type: 'container',
                data: data
            }
        }
        if (obj.constructor.name === 'Object') {
            let data = {}
            for (let k in obj) {
                data[k] = wrapObjToJson(obj[k]);
            }
            return {
                type: 'container',
                data: data
            }
        }

        throw new Error(`wrapObjToJson: Unknown type: ${typeof obj}`);
    }

    if (ObjectSpecifier.hasInstance(obj)) {
        let classOf = ObjectSpecifier.classOf(obj);

        if (classOf === 'application') {
            return {
                type: 'reference',
                objId: cacheObjct(obj),
                className: 'application'
            }
        }

        // If the evaluated object is a plain object, return the evaluated value.
        // WARNING: This may cause problems if the object is a reference to a text or dict.
        //          In that case, the object "can" be interpreted as a plain object but still
        //          has properties that are references to other objects.
        let evaluated = obj();
        if (!ObjectSpecifier.hasInstance(evaluated)) {
            return wrapObjToJson(evaluated);
        }

        return {
            type: 'reference',
            objId: cacheObjct(obj),
            className: classOf
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
    } else if (obj.type === 'container') {
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
callSelf = jsonIOWrapper(callSelf);