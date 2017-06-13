var Home = {
  name: 'Home',
  template: '#home-template'
};

var ServiceListing = {
  name: 'ServiceListing',
  template: '#services-template',
  mounted: function() {
    this.fetchServices();
  },
  data: function() {
    return {
      services: []
    };
  },
  methods: {
    fetchServices: function() {
      this.$http.get('http://172.17.0.2:5023/v1/service').then(response => {
        this.services = response.body;
      }, response => {
        console.error(response.body);
      });
    }
  }
};

var NodesListing = {
  name: 'NodesListing',
  template: '#nodes-template',
  mounted: function() {
    this.fetchNodes();
  },
  data: function() {
    return {
      nodes: []
    };
  },
  methods: {
    fetchNodes: function() {
      this.$http.get('http://172.17.0.2:5023/v1/nodes').then(response => {
        console.log(response.body);
        this.nodes = response.body;
      }, response => {
        console.error(response.body);
      });
    }
  }
};

var BlueprintTemplate = {
  name: 'BlueprintTemplate',
  template: '#blueprint-template',
  data: function() {
    return {
      blueprint: ''
    };
  },
  methods: {
    sendBlueprint: function(event) {
      this.$http.post('http://172.17.0.2:5023/v1/service', this.blueprint, {headers: {'Content-Type': 'application/x-yaml'}}).then(response => {
        console.log(response.body);
      }, response => {
        console.error(response.body);
      });
    }
  }
};

// Create the router
var router = new VueRouter({
	mode: 'hash',
	base: window.location.href,
	routes: [
		{path: '/', component: Home},
		{path: '/services', component: ServiceListing},
    {path: '/nodes', component: NodesListing},
    {path: '/blueprint', component: BlueprintTemplate}
	]
});

const app = new Vue({
  el: "#app",

  router: router,
  data: {
    currentRoute: window.location.pathname
  },

  mounted: function() {

  },

  methods: {
    // onClick: function(item) {
    //   this.$http.post('/api/reset_waitlist_v2', item, function(data) {
    //     this.email = data.email;
    //   })
    // }
  }
});
