
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import appSettings from '../config/config.json';

const apiBasePath = appSettings.api.basePath;

createApp(App)
    .use(router)
    .provide('settings', appSettings)
    .provide('apiResource', (resourceName: string, method: string, id?: number): string => {
        const resource = appSettings.api.resources[resourceName];
        if (resource[method]) {
            switch(method) {
                case 'show':
                case 'delete':
                    return apiBasePath + resource[method] + '/' + id + '/';
                default:
                    return apiBasePath + resource[method];
            }
            
        }
        console.error(`Method '${method}' for resource '${resourceName}' not found`, {resource});
        return '';
    })
    .provide('apiFilter', (resourceName: string, filter: string, ...params: string[]): string => {
        const resource = appSettings.api.resources[resourceName];
        const urlPath = resource['filters'] ? resource['filters'][filter] : null;
        if (urlPath) {
            params = params.reverse().filter(param => param).reverse(); // remove empty params
            const url = apiBasePath + urlPath + (params.length ? ('/' + params.join('/')) : '');
            return url;
        }
        console.error(`Not found filter '${filter}' for '${resourceName}' resource`);
        return '';
    })
    .mount('#app');



