import adapter from '@sveltejs/adapter-auto';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter(),
		csp: {
			mode: "auto",
			directives: {
				"default-src": ["self"],
				"style-src": ["self", "https://rsms.me/inter/inter.css"],
				"font-src": ["self", "https://rsms.me/inter/font-files/ *"],
				"object-src": ["none"],
				"base-uri": ["none"],
				"frame-ancestors": ["none"],
				"referrer": ["no-referrer", "strict-origin-when-cross-origin"],
				"upgrade-insecure-requests": true,
			},
		},
	}
};

export default config;
