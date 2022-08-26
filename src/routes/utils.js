import items from "$lib/data/items.json";

export function sortItems(list) {
    return list.sort((prev, curr) => items[prev.id].sortId - items[curr.id].sortId);
};