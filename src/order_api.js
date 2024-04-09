async function apifetch(endpoint) {
    try {
        const response = await fetch(`http://localhost:5000/api/${endpoint}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch ${endpoint}`);
        }
        const data = await response.json();
        console.log(`Fetched ${endpoint}:`, data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log(`Error fetching ${endpoint}:`, error);
        return [];
    
    }
}

export async function fetchOrders() {
    return apifetch('orders');
}

export async function fetchOrder(id) {
    return apifetch(`orders/${id}`);
}

export async function fetchCompanies() {
    return apifetch('companies');
}

export async function fetchProducts() {
    return apifetch('products');
}

export async function fetchLocations() {
    return apifetch('locations');
}

export async function fetchContacts() {
    return apifetch('contacts');
}

