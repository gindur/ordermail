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
    <img src='/img/logo.png' alt='Nordhaus logo'>
    <Nav navItems={navItems} active={active} on:navChange={navChange} />
</header>

<style>
    header {
        background: #f7f7f7;
        padding: 10px;
    }
    h1 {
        margin: 10px;
        text-align: center;
    }
    img {
        max-width: 180px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

</style>