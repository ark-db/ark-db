import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		csp: {
			mode: "auto",
			directives: {
				"default-src": ["self"],
				"style-src": ["self", "https://rsms.me/inter/*"],
				"script-src": ["nonce-{random}", "unsafe-inline"],
				"object-src": ["none"],
				"base-uri": ["none"],
				"upgrade-insecure-requests": true,
			},
		},
	}
};

export default config;
