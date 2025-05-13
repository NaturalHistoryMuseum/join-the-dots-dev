<script>
import axios from 'axios'

export default {
  data() {
    return {
      data: [],
    }
  },
  methods: {
    fetchData() {
      axios
        .get('http://localhost:5000/api/data/assessment-criterion', { withCredentials: true })
        .then((response) => {
          this.data = response.data
        })
    },
  },
}
</script>
