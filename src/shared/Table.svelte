<script>
  import { Table, Tbody, Thead } from "svelte-atoms";
  import OrderSubtable from "./OrderSubtable.svelte";

  export let data = [];
  // example product data = [{id: 1, name: "product1", price: 100}, {id: 2, name: "product2", price: 200}]
  export let keyField = "id";
  export let expandType = null;
  export let getExpandedContent = null;

  let expandedRows = new Set();
  let expandedContent = {};
  $: expandedRows;

  async function toggleRow(row) {
    const keyValue = row[keyField];
    if (expandedRows.has(keyValue)) {
      expandedRows.delete(keyValue);
    } else {
      expandedRows.add(keyValue);
      if (!expandedContent[keyValue]){
        expandedContent[keyValue] = await getExpandedContent(keyValue);
      }
    }
    expandedRows = new Set(expandedRows);
  }

  let columns = [];
  $: columns = data.length > 0 ? Object.keys(data[0]) : [];

  // Sorting
  let sortColumn = null;
  let sortDirection = "asc";

  function sortData(column) {
    if (sortColumn === column) {
      sortDirection = sortDirection === "asc" ? "desc" : "asc";
    } else {
      sortColumn = column;
      sortDirection = "asc";
    }

    data = [...data].sort((a, b) => {
      if (a[sortColumn] < b[sortColumn])
        return sortDirection === "asc" ? -1 : 1;
      if (a[sortColumn] > b[sortColumn])
        return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }
</script>

<Table>
  {#if data.length > 0}
    <Thead>
      <tr>
        {#each columns as column}
          <th on:click={() => sortData(column)}>{column}</th>
        {/each}
        {#if expandType}
          <th></th>
        {/if}
      </tr>
    </Thead>
  {/if}
  <Tbody>
    {#each data as row}
      <tr on:click={() => toggleRow(row)} >
        {#each Object.values(row) as value}
          <td>{value}</td>
        {/each}
        {#if expandType}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          {#if expandedRows.has(row[keyField])}
            <td>⯆</td>
          {:else}
            <td>⯈</td>
          {/if}
        {/if}
      </tr>
      {#if expandType == "order" && expandedRows.has(row[keyField])}
      <tr>
        <td class="expanded" colspan="{Object.keys(row).length + 1}">
        {#if expandedContent[row[keyField]]}
          <OrderSubtable products={expandedContent[row[keyField]]} />
        {:else}
          <p>Loading...</p>
        {/if}
        </td>
      </tr>
      {/if}
    {/each}
  </Tbody>
</Table>

<style>
  tr:hover td:not(.expanded) {
  background-color: #dcdcdc;
}

.expanded {
  padding: 10px;
}



</style>
