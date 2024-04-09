<!--OrderSubtable.svelte-->
<script>
    export let products = [];
</script>

<table>
    <thead>
        <tr>
            {#if products.length > 0}
                {#each Object.keys(products[0]) as key}
                    <th>{key}</th>
                {/each}
            {/if}
        </tr>
    </thead>
    <tbody>
        {#each products as product}
            <tr>
                {#each Object.values(product) as value}
                    {#if value && value === product["Bild"]}
                        <!-- svelte-ignore a11y-img-redundant-alt -->
                        <td><img src={value.split(',')[0]} alt="product image" style="width: 50px;"/></td>
                    {:else}
                    <td>{value}</td>
                    {/if}
                {/each}
            </tr>
        {/each}
    </tbody>
</table>

