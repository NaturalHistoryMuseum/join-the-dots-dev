<template>
  <p>Please use the following pages to manage users permissions</p>
  <div class="permission-actions">
    <zoa-button
      label="Manage User Permissions"
      @click="$router.push('/user-management')"
    />
    <zoa-button
      kind="alt"
      label="Manage Units Permissions"
      @click="$router.push({ path: '/manage-unit-permissions' })"
    />
  </div>
</template>

<script>
export default {
  name: 'AdminPermissions',
};
</script>

<style scoped>
.permission-actions {
  display: flex;
  gap: 1rem;
}
</style>
