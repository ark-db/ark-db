import adapter from '@sveltejs/adapter-vercel';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		csp: {
			mode: "hash",
			directives: {
				"default-src": ["self"],
				"style-src": ["self", "https://rsms.me/inter/inter.css"],
				"font-src": ["self", "https://rsms.me/inter/font-files/ *"],
				"object-src": ["none"],
				"frame-ancestors": ["none"],
				"base-uri": ["none"],
				"frame-ancestors": ["none"],
				"form-action": ["none"],
				"upgrade-insecure-requests": true,
			},
		},
	}
};

export default config;
