<template>
  <div class="main-page">
    <div class="units-content">
      <div class="actions-bar" v-show="currentUser.role_id > 1">
        <ActionsBtnGroup :force_show="selectedUnitIds.length > 0">
          <DeleteModal
            :selected_units="
              units.filter((unit) =>
                selectedUnitIds.includes(unit.collection_unit_id),
              )
            "
            @update:refreshData="fetchData"
            :included_in_rescore="
              Object.keys(this.open_rescore).length > 0 &&
              rescore_units.some((rescore_unit) =>
                selectedUnitIds.includes(rescore_unit),
              )
            "
          />
          <SplitModal
            v-if="selectedUnitIds.length < 2"
            :selected_unit="
              units.find(
                (unit) => unit.collection_unit_id == selectedUnitIds[0],
              )
            "
            @update:refreshData="fetchData"
            :included_in_rescore="
              Object.keys(this.open_rescore).length > 0 &&
              rescore_units.some((rescore_unit) =>
                selectedUnitIds.includes(rescore_unit),
              )
            "
          />
          <CombineModal
            v-if="selectedUnitIds.length == 0 || selectedUnitIds.length > 1"
            :selected_units="
              units.filter((unit) =>
                selectedUnitIds.includes(unit.collection_unit_id),
              )
            "
            @update:refreshData="fetchData"
            :included_in_rescore="
              Object.keys(this.open_rescore).length > 0 &&
              rescore_units.some((rescore_unit) =>
                selectedUnitIds.includes(rescore_unit),
              )
            "
          />
          <zoa-button label="Add Unit" @click="navAddUnit" />
          <zoa-button
            v-if="currentUser.role_id >= 3"
            kind="alt"
            label="Manage User Permissions"
            @click="$router.push('/user-management')"
          />
          <zoa-button
            kind="alt"
            label="Manage Units Permissions"
            @click="navUnitAssignment"
          />
        </ActionsBtnGroup>
      </div>
      <div class="content-container">
        <!-- Search bar -->
        <SidebarFilter
          :units="units"
          :show_filters="[
            'departments',
            'show_own',
            'unit_id',
            'unit_name',
            'section',
            'division',
            'curators',
          ]"
          :column_direction="true"
          @update:filteredUnits="handleFilteredUnits"
        />
        <div class="table-area">
          <!-- Table -->
          <TableCheckbox
            ref="viewTable"
            :units="filteredUnits"
            :fields="fields"
          >
            <!-- Custom rendering for the name column -->
            <template #cell(name)="row">
              {{ row.value.first }} {{ row.value.last }}
            </template>

            <!-- Actions column -->
            <!-- <template #cell(actions)="row">
              <div class="row-actions">
                <zoa-button @click="viewUnit(row.item)" class="view-btn">
                  View Unit
                </zoa-button>
                <zoa-button class="delete-btn">Delete Unit</zoa-button>
              </div>
            </template> -->
            <template #cell(actions)="row">
              <zoa-button @click="() => viewUnit(row.item)" class="view-btn">
                View Unit
              </zoa-button>
            </template>
          </TableCheckbox>
          <p v-if="filteredUnits.length == 0">No units found.</p>
          <p v-if="filteredUnits.length == 0">
            Note: You can assign units to yourself in the account page (user
            icon in top right of screen).
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActionsBtnGroup from '@/components/ActionsBtnGroup.vue';
import CombineModal from '@/components/modals/CombineModal.vue';
import DeleteModal from '@/components/modals/DeleteModal.vue';
import SplitModal from '@/components/modals/SplitModal.vue';
import SidebarFilter from '@/components/SidebarFilter.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import { currentUser, loadUser } from '@/services/authService';
import { getGeneric } from '@/services/dataService';

export default {
  name: 'ViewUnits',
  components: {
    SidebarFilter,
    ActionsBtnGroup,
    TableCheckbox,
    SplitModal,
    CombineModal,
    DeleteModal,
  },
  data() {
    return {
      currentUser,
      actions: [
        {
          action: 'Delete',
          header: 'Delete Units',
          description:
            'This will remove the selected units. This cannot be undone without contacting an admin.',
        },
        {
          action: 'Split',
          header: 'Split Unit',
          description:
            'This will split the selected units into multiple different units. You will then need to go and edit the meta data of the new units.',
        },
        {
          action: 'Combine',
          header: 'Combine Units',
          description:
            'This will combine the selected units into one new unit. This cannot be undone. (not working yet)',
        },
        {
          action: 'Edit',
          header: 'Bulk Edit Units',
          description:
            'This make changes to the selected units. This cannot be undone. (not working yet)',
        },
      ],
      units: [],
      fields: [
        { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Unit ID', key: 'collection_unit_id' },
        { label: 'Unit Name', key: 'unit_name' },
        // { label: 'Named Collection', key: 'named_collection' },
        { label: 'Section', key: 'section_name' },
        { label: 'Division', key: 'division_name' },
        // { label: 'Department', key: 'department_name' },
        { label: 'Actions', key: 'actions' },
      ],
      filteredUnits: [],
      open_rescore: {},
      rescore_units: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      // Reload the user - this gets the list of assigned units
      loadUser(true);
      // Fetch units
      getGeneric('unit-department').then((response) => {
        // Add selected property to each unit
        this.units = response.map((unit) => ({
          ...unit,
          selected: false,
        }));
      });
      getGeneric('open-rescore').then((response) => {
        this.open_rescore = response.length > 0 ? response[0] : {};
        if (Object.keys(this.open_rescore).length > 0) {
          // Set the rescore session id
          this.rescore_session_id = this.open_rescore.rescore_session_id;
          // Fetch units in this rescore session
          getGeneric(`rescore-units/${this.rescore_session_id}`).then(
            (response) => {
              this.rescore_units = response.map(
                (unit) => unit.collection_unit_id,
              );
            },
          );
        }
      });
    },
    viewUnit(unit) {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: unit.collection_unit_id,
        },
      });
    },
    navAddUnit() {
      this.$router.push({ path: '/view-unit', query: { add_unit: 1 } });
    },
    navUnitAssignment() {
      this.$router.push({ path: '/manage-unit-permissions' });
    },
    handleFilteredUnits(filteredUnits) {
      // Only reset pagination if actual filter logic triggered
      if (!this._internalChange) {
        this.filteredUnits = JSON.parse(JSON.stringify(filteredUnits));
        if (filteredUnits.length > 0) {
          this.$refs.viewTable.resetPage();
        }
      }
    },
  },
  computed: {
    // Computed property to get the selected unit IDs
    selectedUnitIds() {
      return this.filteredUnits
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id);
    },
  },
};
</script>

<style>
.actions-bar {
  text-align: left;
}
.content-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}
.units-content {
  flex: 1;
  width: 100%;
  /* padding: 10px 20px; */
}

.unit-table {
  width: 100%;
}

.customPagination {
  margin: 0 !important;
}

.table-area {
  display: flex;
  flex-direction: column;
  width: 100%;
}

@media (max-width: 768px) {
  .content-container {
    flex-direction: column;
  }
  .unit-table {
    font-size: 0.9rem;
  }
  .mobile-toggle {
    text-align: center;
    margin-bottom: 10px;
  }

  .units-conten {
    padding: 5px 10px;
  }
}
</style>
