import adapter from '@sveltejs/adapter-vercel';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		csp: {
			mode: "auto",
			directives: {
				"default-src": ["self"],
				"style-src": ["self", "unsafe-inline", "https://rsms.me/inter/inter.css"],
				"font-src": ["self", "https://rsms.me/inter/font-files/ *"],
				"object-src": ["none"],
				"base-uri": ["none"],
				"frame-ancestors": ["none"],
				"form-action": ["none"],
				"upgrade-insecure-requests": true,
			},
		},
		version: {
			name: "0.14.6"
		}
	}
};

export default config;
