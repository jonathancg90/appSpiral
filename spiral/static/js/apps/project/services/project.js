projectApp.service('projectService', function() {
    var self = this;
    self.step = 1;
    self.deliveries = [];
    self.detailModel = [];
    self.conditions = [];
    self.detailStaff = [];
    self.payment = {};
    self.duty = {};


    self.set_result = function(result){
        self.id = result.id;
        self.deliveries = result.deliveries;
        self.detailModel = result.detailModel;
        self.detailStaff = result.detailStaff;
        self.conditions = result.conditions;
        self.payment = result.payment;
        self.line = result.line;
        self.productor = result.productor;
        self.agency = result.agency;
        self.director = result.director;
        self.commercial = result.commercial;
        self.startProduction = result.startProduction;
        self.finishProduction = result.finishProduction;
        self.observation = result.observation;
        self.project_code = result.codeUpdate;
        self.typeCasting = result.typeCasting;
        self.ppi = result.ppi;
        self.realized = result.realized;
        self.ppg = result.ppg;
        self.duty = result.duty;
        self.budget = result.budget;
        self.internalBudget = result.internalBudget;
        self.duty = result.duty;

        //Photo
        self.type = result.type;
        self.use = result.use;

        //Representation
        self.event = result.event;
    };

    self.clean = function(line){
        self.deliveries = [];
        self.detailModel = [];
        self.detailStaff = [];
        self.conditions = [];
        self.duty = {};
        self.payment = {};
        self.line = line;
        self.productor = {};
        self.agency = {};
        self.director = {};
        self.commercial = {
            'name': ''
        };
        self.startProduction = undefined;
        self.finishProduction = undefined;
        self.observation = undefined;
        self.project_code = undefined;
        self.typeCasting = {};
        self.ppi = undefined;
        self.realized = undefined;
        self.ppg = undefined;
        self.budget = undefined;
        self.internalBudget = undefined;
    }
});