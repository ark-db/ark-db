<script>
    import { page } from '$app/stores';
    let logo = "./favicon.svg"
</script>

<header>
    <div class="logo">
        <a href="/">
            <img src={logo} alt="ArkDB">
        </a>
    </div>

    <nav>
        <ul>
            <li class:active={$page.url.pathname === '/'}>
                <a href="/">
                    Home
                </a>
            </li>
			<li class:active={$page.url.pathname === '/planner'}>
				<a href="/planner">
                    Upgrade Planner
                </a>
			</li>
        </ul>
    </nav>
</header>

<style>
	header {
		display: flex;
        background: rgb(190, 229, 249);
	}

	.logo {
		width: 3em;
		height: 3em;
	}

	.logo a {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
	}

	.logo img {
		width: 2em;
		height: 2em;
		object-fit: contain;
	}

	nav {
		display: flex;
		justify-content: center;
	}

	ul {
		position: relative;
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
        border-bottom: 3px solid transparent;
	}

    li.active {
        border-bottom: 3px solid skyblue;
        box-sizing: border-box;
    }

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 1em;
		color: black;
		text-decoration: none;
	}
</style>