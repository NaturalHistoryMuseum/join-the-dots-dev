<script setup>
import TestTable from '../components/TestTable.vue'
</script>

<template>
  <div id="test-page">
    <h1>Test Page</h1>

    <!-- Counter Section -->
    <div>
      <h2>Counter</h2>
      <p>Counter: {{ counter }}</p>
      <zoa-toggle-button @click="incrementCounter" label="Increase Counter" />
      <zoa-button @click="resetCounter" label="Reset Counter" />
    </div>

    <!-- Table Section -->
    <div>
      <h2>Item Table</h2>
      <form @submit.prevent="addItem">
        <input v-model="newItem" placeholder="Add a new item" />
        <button type="submit">Add Item</button>
      </form>
      <table border="1">
        <thead>
          <tr>
            <th>#</th>
            <th>Item</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ item }}</td>
            <td>
              <button @click="deleteItem(index)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div>
      <TestTable />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      counter: 0,
      items: ['this is the first one'],
      newItem: '',
    }
  },
  methods: {
    incrementCounter() {
      this.counter++
    },
    addItem() {
      if (this.newItem.trim()) {
        this.items.push(this.newItem.trim())
        this.newItem = ''
      }
    },
    deleteItem(index) {
      this.items.splice(index, 1)
    },
    resetCounter() {
      this.counter = 0
    },
  },
}
</script>

<style>
#test-page {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  text-align: center;
  margin-top: 50px;
}
table {
  margin: 20px auto;
  border-collapse: collapse;
  width: 50%;
}
th,
td {
  padding: 10px;
  text-align: left;
}
button {
  padding: 5px 10px;
  cursor: pointer;
}
</style>
