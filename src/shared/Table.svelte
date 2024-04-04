<script>
  import { Table, Tbody, Thead } from 'svelte-atoms';
  
  export let data = [];

  const deleteRow = (id) => {
    data = data.filter( (row) => row.order_id != id)
  }

</script>
<Table >
  {#if data.length > 0 }
    <Thead>
      <tr>
        {#each Object.entries(data[0]) as [col, _]}
        <th>{col}</th>
        {/each}
      </tr>
    </Thead>
  {/if}
  <Tbody>
    {#each data as row}
      <tr>
        {#each Object.entries(row) as [_,data]}
          <td>{data}</td>
        {/each}
      </tr>
    {/each}
  </Tbody>
</Table>

<style>

</style>