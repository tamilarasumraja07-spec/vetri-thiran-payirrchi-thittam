function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function formatCurrency(value) {

    const number =
        Number(value || 0);

    return "₹" +
        number.toLocaleString(
            "en-IN",
            {
                maximumFractionDigits: 0
            }
        );
}


function renderValue(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }


    if (
        typeof value === "string" ||
        typeof value === "number"
    ) {
        return `<p>${escapeHtml(value)}</p>`;
    }


    if (Array.isArray(value)) {

        return `
            <ul>
                ${
                    value.map(
                        item => `
                            <li>
                                ${renderValue(item)}
                            </li>
                        `
                    ).join("")
                }
            </ul>
        `;
    }


    if (
        typeof value === "object"
    ) {

        return `
            <div class="budget-list">

                ${
                    Object.entries(value)
                    .map(
                        ([key, val]) => {

                            let displayValue =
                                val;

                            if (
                                typeof val === "number" &&
                                (
                                    key === "amount" ||
                                    key === "total" ||
                                    key === "main_piece" ||
                                    key === "accessories" ||
                                    key === "reserve"
                                )
                            ) {
                                displayValue =
                                    formatCurrency(val);
                            }

                            return `
                                <div class="budget-item">

                                    <strong>
                                        ${escapeHtml(
                                            key
                                        )}
                                    </strong>

                                    <span>
                                        ${
                                            typeof displayValue === "object"
                                                ? renderValue(displayValue)
                                                : escapeHtml(displayValue)
                                        }
                                    </span>

                                </div>
                            `;
                        }
                    )
                    .join("")
                }

            </div>
        `;
    }


    return "";
}


function renderRecommendation(
    container,
    response
) {

    const data =
        response.data || {};

    const title =
        data.title ||
        "PocketSmart AI Recommendation";

    const summary =
        data.summary ||
        "Your personalized recommendation is ready.";


    let html = `

        <div class="recommendation">

            <span class="badge">
                ${escapeHtml(
                    response.source || "AI"
                )}
            </span>

            <h2>
                ${escapeHtml(title)}
            </h2>

            <p>
                ${escapeHtml(summary)}
            </p>

    `;


    if (data.budget) {

        html += `

            <div class="recommendation-section">

                <h3>
                    Budget
                </h3>

                ${renderValue(
                    data.budget
                )}

            </div>

        `;
    }


    if (data.shopping_list) {

        html += `

            <div class="recommendation-section">

                <h3>
                    Shopping List
                </h3>

                ${renderValue(
                    data.shopping_list
                )}

            </div>

        `;
    }


    if (data.recommendations) {

        html += `

            <div class="recommendation-section">

                <h3>
                    Recommendations
                </h3>

                ${renderValue(
                    data.recommendations
                )}

            </div>

        `;
    }


    if (data.tips) {

        html += `

            <div class="recommendation-section">

                <h3>
                    Smart Tips
                </h3>

                ${renderValue(
                    data.tips
                )}

            </div>

        `;
    }


    html += `
        </div>
    `;


    container.innerHTML = html;
}


async function logout() {

    await fetch(
        "/api/auth/logout",
        {
            method: "POST"
        }
    );

    window.location.href = "/";
}