<script>
    import {createEventDispatcher} from 'svelte';
	import Nav from '../shared/Nav.svelte';
    export let navItems;
    export let active = "Beställningar";

    const dispatch = createEventDispatcher();
    const navChange =  (e) => {
        active = e.detail;
        dispatch('navChange', active);
    };

</script>

<header>
    <h1>
        <img src='/img/logo.png' alt='Nordhaus logo'>
    </h1>
    <Nav navItems={navItems} active={active} on:navChange={navChange} />
</header>

<style>
    header {
        background: #f7f7f7;
        padding: 20px;
    }
    h1 {
        margin:0;
        text-align: center;
    }

    img {
        max-width: 180px;
    }

</style>