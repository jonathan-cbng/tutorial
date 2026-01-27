<template>
  <div>
    <!-- Search and New Case Button Row -->
    <div class="d-flex align-items-center mb-3">
      <CaseSearchBox @search="onSearch" />
      <!-- <button class="btn btn-success ms-3" @click="onNewCase">
        <i class="bi bi-plus-lg"></i> New Case
      </button> -->
    </div>
    <div v-if="cases && sexes && speciesList.length" class="container-fluid">
      <table class="table table-bordered table-striped table-hover table-sm">
        <thead>
          <tr>
            <th class="min-col-action">Action</th>
            <th class="min-col-wider">Name</th>
            <th class="min-col-wider">Owner</th>
            <th class="min-col">Species</th>
            <th class="min-col-breed-sex" :style="breedMinWidth">Breed</th>
            <th class="min-col-breed-sex" :style="sexMinWidth">Sex</th>
            <th class="min-col">Birthdate</th>
            <th class="min-col-wide">Practice Animal ID</th>
            <th class="min-col-wide">Chip ID</th>
            <th class="notes-col">Notes</th>
          </tr>
        </thead>
        <tbody>
          <CaseCreate
            :species-list="speciesList"
            :breeds="filteredBreeds"
            :sexes="sexes"
            :errors="errors"
            :selected-species="selectedSpecies"
            :breed-min-width="breedMinWidth"
            :sex-min-width="sexMinWidth"
            @add-case="addCase"
            @species-change="onSpeciesChange"
            @update:errors="errors = $event"
          />
          <CaseList
            :case-list="cases"
            :breeds="filteredBreeds"
            :sexes="sexes"
            :species-list="speciesList"
            :selected-species="selectedSpecies"
            :errors="errors"
            :row-errors="rowErrors"
            :clean-row-id="cleanRowId"
            @delete-case="deleteCase"
            @row-species-change="fetchBreedsForSpecies"
            @clean-row-handled="cleanRowId = null"
          />
        </tbody>
      </table>
    </div>
    <!-- Popup Modal -->
    <div v-if="showPopup" class="modal fade show" tabindex="-1" style="display:block; background:rgba(0,0,0,0.3);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">Error</h5>
            <button type="button" class="btn-close btn-close-white" @click="closePopup"></button>
          </div>
          <div class="modal-body">
            <p>{{ popupMessage }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closePopup">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showPopup" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import CaseList from './CaseList.vue';
import CaseCreate from './CaseCreate.vue';
import CaseSearchBox from './CaseSearchBox.vue';
import {
  fetchCases,
  addCase,
  updateCase,
  deleteCase,
  fetchSexes,
  fetchSpecies,
  fetchBreedsBySpecies
} from '../api.js';
import { useApiErrorHandler } from '../api.js';

export default {
  name: 'CaseListView',
  components: { CaseList, CaseCreate, CaseSearchBox },
  setup() {
    const { showPopup, popupMessage, handleError, closePopup } = useApiErrorHandler();
    return { showPopup, popupMessage, handleError, closePopup };
  },
  data() {
    return {
      cases: null,
      sexes: null,
      errors: {},
      rowErrors: {},
      deploymentId: 'production',
      deploymentColour: '#333',
      deploymentName: '',
      speciesList: [],
      breedsBySpecies: {}, // { species: [breed, ...] }
      selectedSpecies: '',
      cleanRowId: null,
      searchQuery: ''
    };
  },
  computed: {
    filteredBreeds() {
      return this.selectedSpecies && this.breedsBySpecies[this.selectedSpecies]
        ? this.breedsBySpecies[this.selectedSpecies]
        : [];
    },
    breedMinWidth() {
      if (!this.filteredBreeds || this.filteredBreeds.length === 0) return '';
      const maxLen = Math.max(...this.filteredBreeds.map(b => b.name.length), 'Select breed...'.length);
      return { minWidth: `${maxLen + 4}ch` };
    },
    sexMinWidth() {
      if (!this.sexes || this.sexes.length === 0) return '';
      const maxLen = Math.max(...this.sexes.map(s => s.length), 'Select sex...'.length);
      return { minWidth: `${maxLen + 4}ch` };
    }
  },
  methods: {
    async fetchCases(query = '') {
      try {
        this.cases = await fetchCases(query);
        // After fetching cases, ensure breeds for all unique species are loaded
        const uniqueSpecies = Array.from(new Set((this.cases || []).map(c => c.breed?.species).filter(Boolean)));
        for (const species of uniqueSpecies) {
          if (!this.breedsBySpecies[species]) {
            await this.fetchBreedsForSpecies(species);
          }
        }
      } catch (err) {
        this.handleError(err, 'Failed to fetch cases');
      }
    },
    async fetchSexes() {
      try {
        this.sexes = await fetchSexes();
      } catch (err) {
        this.handleError(err, 'Failed to fetch sexes');
      }
    },
    async fetchSpecies() {
      try {
        this.speciesList = await fetchSpecies();
      } catch (err) {
        this.handleError(err, 'Failed to fetch species');
      }
    },
    async fetchBreedsForSpecies(species) {
      if (!species || this.breedsBySpecies[species]) return;
      try {
        const breeds = await fetchBreedsBySpecies(species);
        this.breedsBySpecies = { ...this.breedsBySpecies, [species]: breeds };
      } catch (err) {
        // Debug log for troubleshooting
        console.error('Failed to fetch breeds for species:', species, err);
        this.handleError(err, `Failed to fetch breeds for species: ${species}`);
      }
    },
    async addCase(caseData) {
      try {
        await addCase(caseData);
        this.errors = {};
        await this.fetchCases(this.searchQuery);
      } catch (err) {
        if (err.response && err.response.data) {
          this.errors = { ...err.response.data };
        } else {
          this.handleError(err, 'Failed to add case');
        }
      }
    },
    async deleteCase(id) {
      try {
        await deleteCase(id);
        await this.fetchCases(this.searchQuery);
      } catch (err) {
        this.handleError(err, 'Failed to delete case');
      }
    },
    async updateCase(id, caseData) {
      console.log('updateCase called in parent for id:', id, caseData);
      try {
        await updateCase(id, caseData);
        this.rowErrors[id] = {};
        await this.fetchCases(this.searchQuery);
        this.cleanRowId = Number(id); // Always set as number
        console.log('Set cleanRowId:', this.cleanRowId);
      } catch (err) {
        if (err.response && err.response.data) {
          this.rowErrors[id] = err.response.data;
        } else {
          this.handleError(err, 'Failed to update case');
        }
      }
    },
    onUpdateRowErrors({ id, errors }) {
      this.rowErrors = { ...this.rowErrors, [id]: errors };
    },
    async onSpeciesChange(species) {
      this.selectedSpecies = species;
      await this.fetchBreedsForSpecies(species);
    },
    onSearch(query) {
      this.searchQuery = query;
      this.fetchCases(query);
    },
    onNewCase() {
      this.$router.push({ name: 'CaseCreate' });
    },
    scrollToAddCaseRow() {
      this.$refs.caseList?.scrollToAddCaseRow();
    }
  },
  async mounted() {
    await this.fetchSpecies();
    if (this.speciesList.includes('Canine')) {
      this.selectedSpecies = 'Canine';
      await this.fetchBreedsForSpecies('Canine');
    } else if (this.speciesList.length) {
      this.selectedSpecies = this.speciesList[0];
      await this.fetchBreedsForSpecies(this.selectedSpecies);
    }
    await this.fetchSexes();
    await this.fetchCases();
  }
};
</script>
