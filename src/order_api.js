export async function fetchOrders() {
    try {
        const response = await fetch('http://localhost:3000/api/orders');
        if (!response.ok) {
            throw new Error('Failed to fetch orders')
        }
        const data = await response.json();
        console.log('Fetched orders:', data);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching orders:', error)
        return [];
    }
}
export async function fetchCustomers() {
    try {
        const response = await fetch('http://localhost:3000/api/customers');
        if (!response.ok) {
            throw new Error('Failed to fetch customers')
        }
        let data = await response.json();
        data = Object.entries(data);
        console.log('Fetched customers:', data[0]);  // Log the fetched data
        return data;
    } catch (error) {
        console.log('Error fetching customers:', error)
        return [];
    }
}