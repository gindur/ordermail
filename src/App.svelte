<script>
	import Table from './shared/Table.svelte';
	import Modal from './Modal.svelte';
	import Header from './components/Header.svelte'
	import {onMount} from 'svelte';
	import { fetchCustomers, fetchOrders } from './order_api';

  	let showModal = false;
	// Navigation
	let active = "Beställningar";
	let navItems = ["Beställningar", "Kunder"]
	// Order table
	let orders = [];
	$: tableOrders = orders.map(order => ({
		"Ordernummer": order.order_id,
		"Företagsnamn": order.company_name,
		"E-post": order.email_address,
		"Telefon": order.phonenumber,
		"Namn": order.firstname.concat(" ",order.lastname),
		"Datum": order.date_paid
	}));
	//Customers
	let customers = [];
	$: tableCustomers = customers.map(customer => ({
		"Företagsnamn": customer[1].company_name,
		"Antal beställningar": customer[1].nbr_of_orders,
		"Total ordervärde": customer[1].order_total.toFixed(2),
		"Email marketing" : customer[1].email_marketing
	}));

	const toggleModal = () => {
		showModal = !showModal;
	}

	const handleSubmit = () => {
		console.log('submitted');
	}

	const navChange = (e) => {
		active = e.detail;
		console.log("Nav: ", active);
	}

	onMount(async () => {
		orders = await fetchOrders();
		orders = orders.reverse();
		customers = await fetchCustomers();
	});
</script>

<Modal {showModal} on:click={toggleModal}>
	<form on:submit|preventDefault={handleSubmit}>
		<input type="text" placeholder="Företagsnamn">
		<input type="email" placeholder="E-post">
		<button>Lägg till</button>
	</form>
</Modal>

<Header navItems={navItems} active={active} on:navChange={navChange} />

<main>
	
	{#if active === navItems[0]}
		<h1>Välkommen till ordermail</h1>
		<p>Nedan kan du se beställningar och lägga in nya beställningar.</p>
		<button on:click={() => toggleModal()}>Skapa order</button>
		<div class="mainTable">
			<Table data={tableOrders} />
		</div>
	{:else if active === navItems[1]}
		<h1>Customers</h1>
		<div class="mainTable">
			<Table data={tableCustomers}/>
		</div>
	{/if}
	
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: black;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	.mainTable{
		align-items: center;
	}
</style>