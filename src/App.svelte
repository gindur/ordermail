<script>
	import Table from './shared/Table.svelte';
	import Modal from './Modal.svelte';
	import Header from './components/Header.svelte'
	import {onMount} from 'svelte';
	import { fetchCompanies, fetchOrders, fetchContacts, fetchLocations, fetchProducts } from './order_api';

  	let showModal = false;
	// Navigation
	let active = "Beställningar";
	let navItems = ["Beställningar", "Företag", "Kontakter", "Platser", "Produkter"];
	// Order table
	let orders = [];
	$: orderTableData = orders.map(order => ({
		"Ordernummer": order.order_id,
		"Företagsnamn": order.company_name,
		"E-post": order.email_address,
		"Namn": order.first_name?.concat(" ",order.last_name),
		"Värde": order.total_amount.toFixed(2),
		"Antal produkter": order.total_qty,
		"Datum": order.date_paid
	}));
	//Company table
	let companies = [];
	$: companyTableData = companies.map(company => ({
		"Företagsnamn": company.company_name,
		"Antal beställningar": company.nbr_of_orders,
		"Total ordervärde": company.order_total.toFixed(2),
		"Email marketing" : company.email_marketing
	}));

	//contacts table
	let contacts = [];
	$: contactsTableData = contacts.map(contact => ({
		"Namn": contact.first_name?.concat(" ",contact.last_name),
		"Email": contact.email_address,
		"Telefon": contact.phonenumber? contact.phonenumber: "-",
		"Företagsnamn": contact.company_name
	}));

	//locations table
	let locations = [];
	$: locationsTableData = locations.map(location => ({
		"Adress": location.address,
		"Postnummer": location.zipcode,
		"Ort": location.city,
		"Land": location.country,
		"Företagsnamn": location.company_name
	}));
	//products table

	// solve 
	let products = [];
	$: productsTableData = products.map(product => ({
		"SKU": product.sku,
		"Produktnamn": product.title,
		"Pris": product.price.toFixed(2),
		"Inköpspris": product.purchase_price? product.purchase_price.toFixed(2): "-"
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
		const fetchedOrders = await fetchOrders();
		orders = fetchedOrders.data;
		const fetchedCompanies = await fetchCompanies();
		companies = fetchedCompanies.data;
		const fetchedContacts = await fetchContacts();
		contacts = fetchedContacts.data;
		const fetchedLocations = await fetchLocations();
		locations = fetchedLocations.data;
		const fetchedProducts = await fetchProducts();
		products = fetchedProducts.data;
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
			<Table data={orderTableData} />
		</div>
	{:else if active === navItems[1]}
		<h1>Företagskunder</h1>
		<div class="mainTable">
			<Table data={companyTableData}/>
		</div>
	{:else if active === navItems[2]}
		<h1>Kontaktpersoner</h1>
		<div class="mainTable">
			<Table data={contactsTableData}/>
		</div>
	{:else if active === navItems[3]}
		<h1>Leveransadresser</h1>
		<div class="mainTable">
			<Table data={locationsTableData}/>
		</div>
	{:else if active === navItems[4]}
		<h1>Produkter</h1>
		<div class="mainTable">
			<Table data={productsTableData}/>
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