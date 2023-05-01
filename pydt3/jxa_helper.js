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

function isPlainJson(obj) {
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

function wrapObjSpecToJson(objSpec) {
    let evaluated = objSpec();

    let classOf = ObjectSpecifier.classOf(objSpec);
    if (classOf === 'application') {
        return {
            name: objSpec.name(),
            type: 'reference',
            rawId: getObjectId(objSpec),
            objId: cacheObjct(objSpec),
            className: classOf
        }
    }
    if (isPlainJson(evaluated)) {
        if (objSpec instanceof Date) {
            return {
                type: 'value',
                data: objSpec.toISOString()
            }
        }
        return {
            type: 'value',
            data: evaluated
        }
    }

    if (typeof evaluated === 'object') {
        for (let k in evaluated) {
            evaluated[k] = wrapObjSpecToJson(objSpec[k]);
        }
        return {
            type: 'container',
            data: evaluated,
        };
    } 
    
    if (classOf !== undefined) {
        // throw new Error(`Unknown type: ${typeof objSpc}`);
        return {
            type: 'reference',
            objId: cacheObjct(objSpec),
            className: classOf
        }
    } 
    
    
    throw new Error(`Unknown type: ${typeof objSpec}`);
}

function unwrapObjFromJson(obj) {
    if (obj.type === 'value') {
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
    return wrapObjSpecToJson(app);
}
getApplication = jsonIOWrapper(getApplication);

function getProperties(params) {
    let objId = params.objId;
    let names = params.names;
    let obj = objectCacheMap[objId];
    let data = {};
    for (let n of names) {
        let property = obj[n];
        data[n] = wrapObjSpecToJson(property);
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

function runMethod(params) {
    let objId = params.objId;
    let name = params.name;
    let args = params.args;
    for (let i = 0; i < args.length; i++) {
        args[i] = unwrapObjFromJson(args[i]);
    }
    let kwargs = {};
    for (let k in params.kwargs) {
        kwargs[k] = unwrapObjFromJson(params.kwargs[k]);
    }

    let obj = objectCacheMap[objId];
    let result = obj[name](...args, kwargs);
    return wrapObjSpecToJson(result);
}
runMethod = jsonIOWrapper(runMethod);


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
    return wrapObjSpecToJson(result);
}
callSelf = jsonIOWrapper(callSelf);