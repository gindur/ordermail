<script>
    import {createEventDispatcher} from 'svelte';
    const dispatch = createEventDispatcher();
    export let navItems;
    export let active;

</script>

<div class="nav">
    <ul>
        {#each navItems as item}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li on:click={() => dispatch('navChange', item)}>
                <div class:active={item === active}>
                    {item}
                </div>
            </li>
        {/each}
    </ul>
</div>

<style>
    .nav{
        margin-bottom: 10px;
    }
    ul {
        display:flex;
        justify-content: center;
        list-style: none;
        padding:0;
    }

    li {
        margin: 0 16px;
        font-size: 18px;
    }
    .active {
        font-weight: bold;
        text-decoration: underline;
    }

</style>