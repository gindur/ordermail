export async function fetchOrders() {
    try {
        const response = await fetch('http://localhost:5000/api/orders');
        if (!response.ok) {
            throw new Error('Failed to fetch orders');
        }
        const data = await response.json();
        console.log('Fetched orders:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching orders:', error);
        return [];
    }
}
export async function fetchCompanies() {
    try {
        const response = await fetch('http://localhost:5000/api/companies');
        if (!response.ok) {
            throw new Error('Failed to fetch companies');
        }
        const data = await response.json();
        console.log('Fetched companies:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching companies:', error);
        return [];
    }
}

export async function fetchProducts() {
    try {
        const response = await fetch('http://localhost:5000/api/products');
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        const data = await response.json();
        console.log('Fetched products:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching products:', error);
        return [];
    }
}

export async function fetchLocations() {
    try {
        const response = await fetch('http://localhost:5000/api/locations');
        if (!response.ok) {
            throw new Error('Failed to fetch locations');
        }
        const data = await response.json();
        console.log('Fetched locations:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching locations:', error);
        return [];
    }
}

export async function fetchContacts() {
    try {
        const response = await fetch('http://localhost:5000/api/contacts');
        if (!response.ok) {
            throw new Error('Failed to fetch contacts');
        }
        const data = await response.json();
        console.log('Fetched contacts:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching contacts:', error);
        return [];
    }
}
