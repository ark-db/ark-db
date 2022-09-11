import { error, json } from "@sveltejs/kit";
import items from "$lib/data/items.json";

export function GET({ url }) {
    const itemId = url.searchParams.get("id");
    const categories = [...url.searchParams.get("categories")?.split(",") ?? []];
    if (itemId) {
        const itemData = items?.[itemId]
        if (itemData) {
            if (categories.length > 0) {
                return json(
                    Object.fromEntries(
                        Object.entries(itemData)
                              .filter(([k, v]) => categories.includes(k))
                    )
                )
            }
            return json(itemData);
        }
        throw error(400, "Invalid item ID");
    }
    if (categories.length > 0) {
        return json(
            Object.fromEntries(
                Object.entries(items)
                      .map(([id, data]) => ([id, Object.fromEntries(Object.entries(data)
                                                                          .filter(([k, v]) => categories.includes(k)))])))
        )
    }
    return json(items);
};