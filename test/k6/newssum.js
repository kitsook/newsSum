import http from 'k6/http';
import { check, fail, sleep } from 'k6';

const host = 'http://localhost:8080';

export const options = {
    setupTimeout: '180s',
    stages: [
        { duration: '5s', target: 20 },
        { duration: '5s', target: 40 },
        { duration: '5s', target: 80 },
        { duration: '10s', target: 160 },
    ],
};

let sources = [];

function getAllSources() {
    let result = [];
    const res = http.get(`${host}/list`);
    if (res.status == 200) {
        result = JSON.parse(res.body);
    }
    if (res.status != 200 || result.length == 0) {
        fail('failed to retrieve sources for setup');
    }
    return result;
}

function randomRetrieveAllSources() {
    let shuffled = sources
        .map(value => ({ value, sort: Math.random() }))
        .sort((a, b) => a.sort - b.sort)
        .map(({ value }) => value);

    shuffled.forEach((source) => {
        console.log(`Preloading ${source.desc}`);
        const res = http.get(`${host}/${source.path}`);
        check(res, { [`${source.desc} status was 200`]: (r) => r.status == 200 });
    })
}

function randomRetrieveOneSource() {
    const index = Math.floor(Math.random() * sources.length);
    const res = http.get(`${host}/${sources[index].path}`);
    check(res, { [`${sources[index].desc} status was 200`]: (r) => r.status == 200 });
}

// setup (once)
export function setup() {
    sources = getAllSources();
    randomRetrieveAllSources();
}

// cleanup (once)
export function teardown() {
}

export default function () {
    if (sources.length == 0) {
        sources = getAllSources();
    }
    randomRetrieveOneSource();
}

