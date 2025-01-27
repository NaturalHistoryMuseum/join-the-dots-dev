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
      axios.get('http://localhost:5000/api/assessment-criterion').then((response) => {
        console.log(response.data)
        this.data = response.data
      })
    },
  },
}
</script>
