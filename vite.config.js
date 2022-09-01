import { sveltekit } from '@sveltejs/kit/vite';
import path from "path";

/** @type {import('vite').UserConfig} */
const config = {
	plugins: [sveltekit()],
	resolve: {
		alias: {
			"@stores": path.resolve("./src/routes/stores.js"),
			"@utils": path.resolve("./src/routes/utils.js"),
		},
	},
};

export default config;
