const chatBody = document.getElementById("chatBody");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");

let lastUserQuery = "";

// 🔥 SAFE GLOBAL STATE (IMPORTANT FIX)
let lastResult = {
    department: "General",
    priority: "Low",
    solution: ""
};

/* ================= USER MESSAGE ================= */
function addUserBubble(text) {
    const div = document.createElement("div");
    div.className = "chat-bubble user";
    div.textContent = text;

    chatBody.appendChild(div);
    scrollToBottom();
}

/* ================= BOT MESSAGE ================= */
function addBotBubble(result) {

    // 🔥 SAVE RESULT GLOBALLY (MAIN FIX)
    lastResult = {
        department: result.department || "General",
        priority: result.priority || "Low",
        solution: result.solution || ""
    };

    const div = document.createElement("div");
    div.className = "chat-bubble bot";

    div.innerHTML = `
        <div><strong>Department:</strong> ${lastResult.department}</div>
        <div class="mt-1"><strong>Solution:</strong> ${lastResult.solution}</div>
        <div class="mt-1"><strong>Priority:</strong> ${lastResult.priority}</div>

        <div class="mt-2">Was your issue resolved?</div>

        <div class="mt-2 d-flex gap-2">
            <button class="btn btn-sm btn-outline-success btn-resolved">YES</button>
            <button class="btn btn-sm btn-outline-danger btn-not-resolved">NO</button>
        </div>
    `;

    chatBody.appendChild(div);

    /* ================= YES BUTTON ================= */
    div.querySelector(".btn-resolved").addEventListener("click", function () {

        div.querySelectorAll("button").forEach(b => b.disabled = true);

        const msg = document.createElement("div");
        msg.className = "chat-bubble bot";
        msg.textContent = "✅ Issue Resolved Successfully";

        chatBody.appendChild(msg);

        scrollToBottom();
    });

    /* ================= NO BUTTON (CREATE TICKET) ================= */
    div.querySelector(".btn-not-resolved").addEventListener("click", async function () {

        div.querySelectorAll("button").forEach(b => b.disabled = true);

        try {
            const response = await fetch("/create_ticket", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    issue: lastUserQuery,
                    department: lastResult.department,
                    priority: lastResult.priority
                })
            });

            const data = await response.json();

            if (data.error) {
                const msg = document.createElement("div");
                msg.className = "chat-bubble bot";
                msg.textContent = "Please login first.";
                chatBody.appendChild(msg);
                return;
            }

            const ticketMsg = document.createElement("div");
            ticketMsg.className = "chat-bubble bot";

            ticketMsg.innerHTML = `
                <strong>Ticket Created Successfully</strong><br>
                Ticket ID: SMIU-2026-${String(data.ticket_id).padStart(4, "0")}<br><br>
                Redirecting to Tickets Page...
            `;

            chatBody.appendChild(ticketMsg);

            setTimeout(() => {
                window.location.href = "/tickets";
            }, 2000);

        } catch (err) {
            console.error(err);

            const msg = document.createElement("div");
            msg.className = "chat-bubble bot";
            msg.textContent = "Ticket creation failed.";

            chatBody.appendChild(msg);
        }

        scrollToBottom();
    });

    scrollToBottom();
}

/* ================= SCROLL ================= */
function scrollToBottom() {
    chatBody.scrollTop = chatBody.scrollHeight;
}

/* ================= CHAT SEND ================= */
chatForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = chatInput.value.trim();
    if (!text) return;

    lastUserQuery = text;

    addUserBubble(text);
    chatInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: text
            })
        });

        const result = await response.json();

        console.log("BOT RESPONSE:", result);

        if (result.found) {
            addBotBubble({
                department: result.department,
                solution: result.solution,
                priority: result.priority
            });
        } else {
            addBotBubble({
                department: "General Support",
                solution: result.message || "No answer found",
                priority: "Low"
            });
        }

    } catch (error) {
        console.error(error);

        addBotBubble({
            department: "System",
            solution: "Backend connection failed.",
            priority: "High"
        });
    }
});