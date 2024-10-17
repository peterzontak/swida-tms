type OptionsArgsType = { method: string; headers?: HeadersInit; data?: object };
type OptionsType = { method: string; headers: HeadersInit; body?: string };

const extractTextFromHTML = (html) => {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    return doc.body.innerText.replace(/\n+/g, '\n');
}

const parseResponse = async (response: Response) => {
    const status = response.status;
    const url = response.url;
    const raw = await response.text();
    let json: object|null = null;


    try {
        json = JSON.parse(raw);
    }
    catch (error) {
        console.group("Error parsing JSON");
        console.info({ url, status });
        console.info(extractTextFromHTML(raw));
        console.log({ raw, error });
        console.groupEnd();
        return null;
    }

    if (!response.ok) {
        console.group("API Error");
            console.error(`HTTP error! Status: ${status}`);
            console.warn({
                statusText: response.statusText,
                redirected: response.redirected
            });
            console.log({url});
            console.log(json);
            console.log({raw});
            if(json && typeof json === 'object' && 'error' in json) alert(json.error);
        console.groupEnd();
    }

    return json;
};

const createOptions = ({ method, headers = {}, data = {} }: OptionsArgsType): OptionsType => {
    const options: OptionsType = {
        method,
        headers: {
            "Content-Type": "application/json",
            ...headers,
        },
    };
    
    if (method === 'POST' || method === 'PUT') {
        options.body = JSON.stringify(data);
    }
    // console.log({options});
    
    return options;
};

// GET request
export const getJson = async (url: string): Promise<any> => {
    try {
        const res = await fetch(url);
        return await parseResponse(res);
    } catch (error) {
        console.error("There was an error fetching the data!", error);
    }
    return null;
};

// POST request
export const postJson = async (url: string, data: object): Promise<any> => {
    // console.log({data});
    
    try {
        const options = createOptions({
            method: 'POST',
            data,
        });
        // console.log({options});
        const res = await fetch(url, options);
        return await parseResponse(res);
    } catch (error) {
        console.group("API Error");
            console.error("There was an error posting the data!");
            console.info({url, data, error});
        console.groupEnd();
    }
    return null;
};

// PUT request
export const putJson = async (url: string, data: object): Promise<any> => {
    try {
        const options = createOptions({
            method: 'PUT',
            data,
        });
        const res = await fetch(url, options);
        return await parseResponse(res);
    } catch (error) {
        console.group("API Error");
            console.error("There was an error updating the data!");
            console.info({url, data, error});
        console.groupEnd();
    }
    return null;
};

// DELETE request
export const deleteJson = async (url: string): Promise<any> => {
    try {
        const options = createOptions({
            method: 'DELETE',
        });
        const res = await fetch(url, options);
        return await parseResponse(res);
    } catch (error) {
        console.group("API Error");
            console.error("There was an error deleting the data!");
            console.info({url, error});
        console.groupEnd();
    }
    return null;
};
