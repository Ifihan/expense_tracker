// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Fetch and display expenses on the dashboard
    if (document.getElementById('expense-table-body')) {
        fetchExpenses();
    }
});

async function fetchExpenses() {
    try {
        const response = await fetch('/api/expenses');
        const expenses = await response.json();
        displayExpenses(expenses);
        updateTotalAmount(expenses);
    } catch (error) {
        console.error('Error fetching expenses:', error);
    }
}

function displayExpenses(expenses) {
    const tableBody = document.getElementById('expense-table-body');
    tableBody.innerHTML = '';

    expenses.forEach(expense => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${expense.date}</td>
            <td>${expense.category}</td>
            <td>$${expense.amount.toFixed(2)}</td>
            <td>
                <a href="/edit_expense/${expense.id}">Edit</a>
                <button onclick="deleteExpense(${expense.id})">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

function updateTotalAmount(expenses) {
    const totalAmount = expenses.reduce((sum, expense) => sum + expense.amount, 0);
    document.getElementById('total-amount').textContent = totalAmount.toFixed(2);
}

async function deleteExpense(id) {
    if (confirm('Are you sure you want to delete this expense?')) {
        try {
            const response = await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
            if (response.ok) {
                fetchExpenses();
            } else {
                console.error('Error deleting expense');
            }
        } catch (error) {
            console.error('Error deleting expense:', error);
        }
    }
}