projectApp.service('projectService', function() {
    var self = this;
    self.step = 1;
    self.deliveries = [];
    self.detailModel = [];
    self.conditions = [];
    self.detailStaff = [];
    self.payment = {};


    self.set_result = function(result){
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
        self.ppg = result.ppg;
        self.budget = result.budget;
        self.internalBudget = result.internalBudget;
    };

    self.clean = function(line){
        self.deliveries = [];
        self.detailModel = [];
        self.detailStaff = [];
        self.conditions = [];
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
        self.ppg = undefined;
        self.budget = undefined;
        self.internalBudget = undefined;
    }
});