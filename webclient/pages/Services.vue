<template>
  <main-layout>
  <table class="table table-bordered" id="user">
    <tr>
      <td>
        <b>ID</b>
      </td>
      <td>
        <b>Name</b>
      </td>
      <td>
        <b>Action</b>
      </td>
      <td>
        <b>Node Type</b>
      </td>
      <td>
        <b>State</b>
      </td>
      <td>
        <b>State Message</b>
      </td>
    </tr>
    <div>
      <tr v-for="service in services">
        <td>
          {{ service.id }}
        </td>
        <td>
          {{ service.name }}
        </td>
        <td>
          {{ service.action }}
        </td>
        <td>
          {{ service.node_type }}
        </td>
        <td>
          {{ service.state }}
        </td>
        <td>
          {{ service.state_message }}
        </td>
      </tr>
    </div>
  </table>
  </main-layout>
</template>

<script>
  import MainLayout from '../layouts/Main.vue'
  export default {
    components: {
      MainLayout
    }
  }
</script>
