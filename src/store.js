// store.js
import { writable } from 'svelte/store';

export const currentMenu = writable(1);  // Default to the first menu item
