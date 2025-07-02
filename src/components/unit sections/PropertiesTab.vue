<template>
  <!-- Time Period To -->
  <div class="row">
    <div class="col-md-6">
      <div class="row">
        <h4 class="subheading">Time Period To</h4>
        <div class="col-md-6 field">
          <zoa-input
            zoa-type="dropdown"
            label="Geological Time Period To"
            :config="{ options: geological_time_period_options }"
            v-model="unit_value.geological_time_period_to_id"
            @change="
              () => {
                setTimeTo();
                handleFieldChange(
                  'geological_time_period_to_id',
                  unit_value.geological_time_period_to_id,
                );
              }
            "
            v-if="allow_edit"
          />
          <div v-else>
            <zoa-input
              zoa-type="empty"
              label="Geological Time Period To"
              class="comments-title"
            />
            <p
              v-if="
                geological_time_period_options.length > 0 &&
                unit_value.geological_time_period_to_id
              "
              class="view-field"
            >
              {{
                geological_time_period_options.find(
                  (option) =>
                    option.value == unit_value.geological_time_period_to_id,
                ).label
              }}
            </p>
          </div>
        </div>
        <div class="col-md-6 field">
          <zoa-input
            zoa-type="empty"
            label="Time To Rank"
            class="comments-title"
          />
          <p class="view-field">{{ current_time_to.rank }}</p>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <div class="row">
        <h4 class="subheading">Time Period From</h4>
        <div class="col-md-6 field">
          <zoa-input
            zoa-type="dropdown"
            label="Geological Time Period From"
            :config="{ options: geological_time_period_options }"
            v-model="unit_value.geological_time_period_from_id"
            @change="
              () => {
                setTimeFrom();
                handleFieldChange(
                  'geological_time_period_from_id',
                  unit_value.geological_time_period_from_id,
                );
              }
            "
            v-if="allow_edit"
          />
          <div v-else>
            <zoa-input
              zoa-type="empty"
              label="Geological Time Period From"
              class="comments-title"
            />
            <p
              v-if="
                geological_time_period_options.length > 0 &&
                unit_value.geological_time_period_from_id
              "
              class="view-field"
            >
              {{
                geological_time_period_options.find(
                  (option) =>
                    option.value == unit_value.geological_time_period_from_id,
                ).label
              }}
            </p>
          </div>
        </div>
        <div class="col-md-6 field">
          <zoa-input
            zoa-type="empty"
            label="Time From Rank"
            class="comments-title"
          />
          <p class="view-field">{{ current_time_from.rank }}</p>
        </div>
      </div>
    </div>
  </div>
  <div class="row">
    <h4 class="subheading">Geographic Origin</h4>
    <div class="col-md-3 field">
      <zoa-input
        zoa-type="dropdown"
        label="Geographic Origin Name"
        :config="{ options: geographic_origin_options }"
        v-model="unit_value.geographic_origin_id"
        @change="
          () => {
            setCurrentGeographicOrigin();
            handleFieldChange(
              'geographic_origin_id',
              unit_value.geographic_origin_id,
            );
          }
        "
        v-if="allow_edit"
      />
      <div v-else>
        <zoa-input
          zoa-type="empty"
          label="Geographic Origin Name"
          class="comments-title"
        />
        <p
          v-if="
            geographic_origin_options.length > 0 &&
            unit_value.geographic_origin_id
          "
          class="view-field"
        >
          {{
            geographic_origin_options.find(
              (option) => option.value == unit_value.geographic_origin_id,
            ).label
          }}
        </p>
      </div>
    </div>
    <div class="col-md-3 field">
      <zoa-input zoa-type="empty" label="Region Type" class="comments-title" />
      <p class="view-field">{{ current_geographic_origin.region_type }}</p>
    </div>
  </div>
  <!-- Taxon -->
  <div class="row">
    <h4 class="subheading">Taxon</h4>
    <div class="col-md-3 field">
      <zoa-input
        zoa-type="textbox"
        label="Informal Taxon"
        v-model="unit_value.infomal_taxon"
        v-if="allow_edit"
      />
      <div v-else>
        <zoa-input
          zoa-type="empty"
          label="Informal Taxon"
          class="comments-title"
        />
        <p class="view-field">{{ unit_value.infomal_taxon }}</p>
      </div>
    </div>
    <div class="col-md-3 field">
      <zoa-input
        zoa-type="dropdown"
        label="Taxon Name"
        :config="{ options: taxon_options }"
        v-model="unit_value.taxon_id"
        @change="
          () => {
            setCurrentTaxon();
            handleFieldChange('taxon_id', unit_value.taxon_id);
          }
        "
        v-if="allow_edit"
      />
      <div v-else>
        <zoa-input zoa-type="empty" label="Taxon Name" class="comments-title" />
        <p
          v-if="taxon_options.length > 0 && unit_value.taxon_id"
          class="view-field"
        >
          {{
            taxon_options.find((option) => option.value == unit_value.taxon_id)
              .label
          }}
        </p>
      </div>
    </div>
    <div class="col-md-3 field">
      <zoa-input zoa-type="empty" label="Taxon Rank" class="comments-title" />
      <p class="view-field">
        {{ current_taxon.taxon_rank }}
      </p>
    </div>
    <div class="col-md-3 field">
      <zoa-input
        zoa-type="empty"
        label="External Ref Name"
        class="comments-title"
      />
      <p class="view-field">{{ current_taxon.external_ref_name }}</p>
    </div>
    <div class="col-md-3 field">
      <zoa-input
        zoa-type="empty"
        label="External Ref Id"
        class="comments-title"
      />
      <p class="view-field">{{ current_taxon.external_ref_id }}</p>
    </div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'PropertiesTab',
  props: {
    unit: Object,
    department_id: Number,
    handleFieldChange: Function,
    allow_edit: Boolean,
  },
  data() {
    return {
      geographic_origin_options: [],
      geological_time_period_options: [],
      current_geographic_origin: {},
      current_time_from: {},
      current_time_to: {},
      taxon_options: [],
      taxon_all_options: [],
      current_taxon: {
        value: null,
        taxon_name: null,
        taxon_rank: '',
        external_ref_name: null,
        external_ref_id: null,
      },
    };
  },
  computed: {
    unit_value: {
      get() {
        return this.unit;
      },
      set(value) {
        this.$emit('updateUnit', value);
      },
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      getGeneric(`all-geographic-origin`).then((response) => {
        this.geographic_origin_options = response.map((geographic_origin) => ({
          ...geographic_origin,
          label: geographic_origin.geographic_origin_name,
          value: geographic_origin.geographic_origin_id,
        }));
        this.setCurrentGeographicOrigin();
      });
      getGeneric(`all-geological-time-period`).then((response) => {
        this.geological_time_period_options = response.map(
          (geological_time_period) => ({
            ...geological_time_period,
            value: geological_time_period.geological_time_period_id,
            label: geological_time_period.period_name,
          }),
        );
        this.setTimeFrom();
      });
      getGeneric(`all-taxon`).then((response) => {
        this.taxon_all_options = response.map((taxon) => ({
          ...taxon,
          value: taxon.taxon_id,
          label: `${taxon.taxon_name} (${taxon.taxon_rank})`,
        }));
        this.setCurrentTaxon();
        this.filterTaxonOptions();
      });
    },
    setCurrentGeographicOrigin() {
      if (this.unit.geographic_origin_id == null) {
        this.current_geographic_origin = {
          value: null,
          geographic_origin_name: null,
          region_type: null,
        };
      } else {
        this.current_geographic_origin = this.geographic_origin_options.filter(
          (geographic_origin) =>
            geographic_origin.geographic_origin_id ==
            this.unit.geographic_origin_id,
        )[0];
      }
    },
    setTimeFrom() {
      if (this.unit.geological_time_period_from_id == null) {
        this.current_time_from = {
          value: null,
          geological_time_period_from_id: null,
          period_name: null,
        };
      } else {
        this.current_time_from = this.geological_time_period_options.filter(
          (geological_time_period) =>
            geological_time_period.geological_time_period_id ==
            this.unit.geological_time_period_from_id,
        )[0];
      }
    },
    setTimeTo() {
      if (this.unit.geological_time_period_to_id == null) {
        this.current_time_to = {
          value: null,
          geological_time_period_to_id: null,
          period_name: null,
        };
      } else {
        this.current_time_to = this.geological_time_period_options.filter(
          (geological_time_period) =>
            geological_time_period.geological_time_period_id ==
            this.unit.geological_time_period_to_id,
        )[0];
      }
    },
    setCurrentTaxon() {
      if (this.unit.taxon_id == null) {
        this.current_taxon = {
          value: null,
          taxon_name: null,
          taxon_rank: null,
          external_ref_name: null,
          external_ref_id: null,
        };
      } else {
        this.current_taxon = this.taxon_all_options.filter(
          (taxon) => taxon.taxon_id == this.unit.taxon_id,
        )[0];
      }
    },
    filterTaxonOptions() {
      this.taxon_options = this.taxon_all_options.filter(
        (taxon) => taxon.department_id == this.department_id,
      );
    },
  },
};
</script>

<style></style>
