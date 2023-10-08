<!-- <template>
  <div class="skills-filter">
    <h2>Skills Filter</h2>
    <div v-for="skill in uniqueSkills" :key="skill">
      <label>
        <input type="checkbox" v-model="selectedSkills" :value="skill" @change="filterListings">
        {{ skill }}
      </label>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    listings: Array, // Array of listings with 'Skill_Name' attribute
  },
  data() {
    return {
      selectedSkills: [], // Selected skills
    };
  },
  computed: {
    uniqueSkills() {
      // Get a unique list of skills from listings
      const skillsSet = new Set();
      this.listings.forEach(listing => {
        if (listing.Skill_Name) {
          skillsSet.add(listing.Skill_Name);
        }
      });
      return Array.from(skillsSet);
    },
  },
  methods: {
    filterListings() {
      // Emit the selected skills to the parent component
      this.$emit('filter', this.selectedSkills);
    },
  },
};
</script>
   -->

   <template>
    <div class="skills-filter">
      <h2>Skills Filter</h2>
      <select v-model="selectedSkill" @change="filterListings">
        <option value="">Select a skill</option>
        <option v-for="skill in uniqueSkills" :key="skill" :value="skill">{{ skill }}</option>
      </select>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      listings: Array, // Array of listings with 'Skill_Name' attribute
    },
    data() {
      return {
        selectedSkill: '', // Selected skill
      };
    },
    computed: {
      uniqueSkills() {
        // Get a unique list of skills from listings
        const skillsSet = new Set();
        this.listings.forEach(listing => {
          if (listing.Skill_Name) {
            skillsSet.add(listing.Skill_Name);
          }
        });
        return Array.from(skillsSet);
      },
    },
    methods: {
      filterListings() {
        // Emit the selected skill to the parent component
        this.$emit('filter', this.selectedSkill);
      },
    },
  };
  </script>
  