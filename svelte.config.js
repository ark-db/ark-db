import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		csp: {
			mode: "auto",
			directives: {
			    "script-src": ["self"],
				"upgrade-insecure-requests": true,
			},
		},
	}
};

export default config;
