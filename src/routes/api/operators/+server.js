import { error, json } from "@sveltejs/kit";
import operators from "$lib/data/operators.json";

export function GET({ url }) {
    const charId = url.searchParams.get("id");
    const categories = [...url.searchParams.get("categories")?.split(",") ?? []];
    if (charId) {
        const charData = operators?.[charId]
        if (charData) {
            if (categories.length > 0) {
                return json(
                    Object.fromEntries(
                        Object.entries(charData)
                              .filter(([k, v]) => categories.includes(k))
                    )
                )
            }
            return json(charData);
        }
        throw error(400, "Invalid character ID");
    }
    if (categories.length > 0) {
        return json(
            Object.fromEntries(
                Object.entries(operators)
                      .map(([id, data]) => ([id, Object.fromEntries(Object.entries(data)
                                                                          .filter(([k, v]) => categories.includes(k)))])))
        )
    }
    return json(operators);
};