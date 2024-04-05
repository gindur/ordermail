<script>
  import { Table, Tbody, Thead } from 'svelte-atoms';
  
  export let data = [];
  let columns = [];
  $: columns = data.length > 0 ? Object.keys(data[0]) : [];

  let sortColumn = null;
  let sortDirection = 'asc';

  function sortData(column) {
    if (sortColumn === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn = column;
      sortDirection = 'asc';
    }

    data = [...data].sort((a, b) => {
      if (a[sortColumn] < b[sortColumn]) return sortDirection === 'asc' ? -1 : 1;
      if (a[sortColumn] > b[sortColumn] ) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  };

</script>
<Table >
  {#if data.length > 0 }
    <Thead>
      <tr>
        {#each columns as column}
        <th on:click={() => sortData(column)}>{column}</th>
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