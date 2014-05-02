this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-budgetline"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<td>\n    <div data-subview=\"blName\"></div>\n</td>\n<td>\n    <div data-subview=\"blAmount\"></div>\n</td>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return " show-full-ui";
  }

function program3(depth0,data) {
  
  
  return "<span class=\"toggle-triangle\">▶</span>";
  }

  buffer += "<table data-lead=\"";
  if (stack1 = helpers.lead) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.lead); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" data-start=\"";
  if (stack1 = helpers.start_date) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.start_date); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" data-end=\"";
  if (stack1 = helpers.end_date) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.end_date); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"\n    class=\"result-overview-table level-5";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <tbody>\n    <tr>\n        <td class=\"overview-minmax unselectable\">";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n        <td class=\"overview-title\">\n        <div data-subview=\"activityName\"></div>\n        </td>\n        <td class=\"overview-description status-background\">\n            <div data-subview=\"activityDescription\"></div>\n        </td>\n        <td class=\"overview-rating\"></td>\n    </tr>\n    <tr class=\"activity-details-row\">\n        <td colspan=\"4\" class=\"activity-details\">\n            <ul>\n                <li>\n                    <h3 class=\"list-label\">Timing</h3>\n                    <div class=\"list-content\">\n                        <div class=\"half-wide centered-content\">\n                            <h4>Start</h4>\n                            <span class=\"activity-timing activity-start\">\n                                <div data-subview=\"activityStartDate\"></div>\n                            </span>\n                        </div>\n                        <div class=\"half-wide centered-content\">\n                            <h4>End</h4>\n                            <span class=\"activity-timing activity-end\">\n                                <div data-subview=\"activityEndDate\"></div>\n                            </span>\n                        </div>\n                    </div>\n                </li>\n                <li>\n                    <h3 class=\"list-label\">Deliverables</h3>\n                    <div class=\"list-content\">\n                            <div data-subview=\"activityDeliverables\"></div>\n                    </div>\n                </li>\n                <li>\n                    <h3 class=\"list-label\">Lead</h3>\n                    <div class=\"list-content\">\n                            <div data-subview=\"activityLead\"></div>\n                    </div>\n                </li>\n                <li class=\"hide-status-history\">\n                    <h3 class=\"list-label\">\n                        <span class=\"status-minmax unselectable\">\n                            <span class=\"toggle-triangle\">▶</span>\n                        </span> Status\n                    </h3>\n                    <div class=\"list-content\">\n                            <div data-subview=\"activityStatusUpdates\"></div>\n                    </div>\n                </li>\n                <li>\n                    <h3 class=\"list-label\">TA</h3>\n                    <div class=\"list-content\">\n                        <h4>Total budget</h4>\n                        <p class=\"ta-lines-total move-right prominent\"></p>\n                        <table class=\"ta-lines-table\">\n                            <thead>\n                                <tr>\n                                    <th>Type</th>\n                                    <th>Name</th>\n                                    <th>Band</th>\n                                    <th>Start</th>\n                                    <th>End</th>\n                                    <th>Days</th>\n                                    <th>Amount</th>\n                                </tr>\n                            </thead>\n                        </table>\n                        <div data-subview=\"activityTALines\"></div>\n                    </div>\n                </li>\n                <li>\n                    <h3 class=\"list-label\">Other</h3>\n                    <div class=\"list-content\">\n                        <h4>Total budget</h4>\n                        <p class=\"budget-lines-total move-right prominent\"></p>\n                        <table class=\"budget-lines-table\">\n                            <thead>\n                                <tr>\n                                    <th>Name</th>\n                                    <th>Amount</th>\n                                </tr>\n                            </thead>\n                        </table>\n                        <div data-subview=\"activityBudgetLines\"></div>\n                    </div>\n                </li>\n            </ul>\n        </td>\n    </tr>\n    </tbody>\n</table>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-statuscontainer"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, self=this;

function program1(depth0,data) {
  
  
  return "\n<div data-subview=\"statusUpdate\"></div>\n";
  }

  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n<div class=\"status-history-wrap\">\n    <div data-subview=\"statusHistory\"></div>\n</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-statushistory"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<td>";
  if (stack1 = helpers.code_name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.code_name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n<td>";
  if (stack1 = helpers.user_name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.user_name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td>";
  if (stack1 = helpers.date) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.date); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-statusupdate"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n                <option value=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = (depth0 && depth0.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n            ";
  return buffer;
  }

  buffer += "<div class=\"status-input\">\n    <div class=\"status-row clearfix\">\n        <span class=\"status-code\">\n            <select name=\"code\">\n            ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.codes), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            </select>\n        </span>\n        <div class=\"status-description\">\n            <div data-field=\"description\" placeholder=\"Add description\" class=\"description rte addeditor\"></div>\n        </div>\n        <span class=\"status-date\">\n            <input type=\"text\" name=\"date\" value=\"";
  if (stack1 = helpers.today) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.today); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" class=\"addpicker\" />\n        </span>\n\n    </div>\n    <div class=\"status-row move-right clearfix\">\n        <input type=\"submit\" class=\"add\" value=\"Update\" />\n        <input type=\"submit\" class=\"cancel\" value=\"Cancel\" />\n    </div>\n</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["activity-taline"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<td>\n    <div data-subview=\"taType\"></div>\n</td>\n<td> \n    <div data-subview=\"taName\"></div>\n</td>\n<td>\n    <div data-subview=\"taBand\"></div>\n</td>\n<td> \n    <div data-subview=\"taStart\"></div>\n</td>\n<td> \n    <div data-subview=\"taEnd\"></div>\n</td>\n<td> \n    <div data-subview=\"taDays\"></div>\n</td>\n<td> \n    <div data-subview=\"taAmount\"></div>\n</td>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["addone-list-view"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<div data-subview=\"itemView\" data-subview-id=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></div>\n";
  return buffer;
  }

  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n<div data-subview=\"itemView\" data-subview-id=\"new\"></div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["assumption-detail"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add assumption";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"description\" \n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.description), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.description), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-date"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add date";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<span data-name=\"";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\"\n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</span>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-deliverables"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.deliverables) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.deliverables); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add deliverables";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"deliverables\" \n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.deliverables), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.deliverables), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-description"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add description";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"description\" \n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.description), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.description), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-field"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "Click to add ";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1);
  return buffer;
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"";
  if (stack1 = helpers.field_name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.field_name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" \n    class=\"heading ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n    >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-name"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add<br>sub-indicator";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"name\" \n    class=\"heading ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.name), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n    >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.name), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-rating"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.color) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.color); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  
  return "notrated";
  }

function program9(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program11(depth0,data) {
  
  
  return "Not rated. Click to rate";
  }

  buffer += "<div data-name=\"rating\" \n    class=\"heading ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\">\n    <div class=\"display-rating-value ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.color), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n        title=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.color), {hash:{},inverse:self.program(11, program11, data),fn:self.program(9, program9, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"></div>\n</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["editable-title"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add title";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<h2 data-name=\"name\" \n    class=\"heading ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.name), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n    >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.name), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</h2>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["export-data"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<option value=\"";
  if (stack1 = helpers.start) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.start); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</option>\n";
  return buffer;
  }

  buffer += "Export logframe data for period:\n<select id=\"export-data\">\n<option value=\"\">----</option>\n";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.periods), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</select>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["indicator-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div class=\"indicator-detail\">\n    <div data-subview=\"indicatorName\"></div>\n    <div data-subview=\"indicatorDescription\"></div>\n</div>\n<div class=\"indicator-data\">\n    <div class=\"indicator-data-table\">\n    <div data-subview=\"targetsTable\"></div>\n    </div>\n    <div class=\"indicator-source\">\n        <h3>Source</h3>\n        <div data-subview=\"indicatorSource\"></div>\n    </div>\n</div>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["indicator-source"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.source) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.source); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add source";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"source\" \n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.source), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.source), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["lead-select"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <option value=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">"
    + escapeExpression(((stack1 = (depth0 && depth0.name)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</option>\n    ";
  return buffer;
  }

  buffer += "<select id=\"filter-by-lead\" name=\"filter-by-lead\" class=\"filter-lead\">\n    ";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.option_list), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</select>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["list-view"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<div data-subview=\"itemView\" \n     data-subview-id=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></div>\n";
  return buffer;
  }

  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["milestone-table-heading-row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<th data-subview=\"itemView\" \n     data-subview-id=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></th>\n";
  return buffer;
  }

  buffer += "<th></th>\n";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["milestone-table-heading"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<div data-name=\"name\">";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["milestone-table"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<table>\n    <thead>\n        <tr data-subview=\"milestoneRow\"></tr>\n    </thead>\n    <div data-subview=\"subindicatorRows\"></div>\n</table>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-actual-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div data-subview=\"valueView\"></div>\n<div data-subview=\"evidenceView\"></div>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-actual-evidence"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.evidence) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.evidence); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add evidence";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"evidence\" \n    class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.evidence), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n    >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.evidence), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-data-entry-row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<td>\n    ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.col), {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n</td>\n";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n    <div data-subview=\"itemView\" data-row=\""
    + escapeExpression(((stack1 = (depth0 && depth0.row)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\" data-col=\""
    + escapeExpression(((stack1 = (depth0 && depth0.col)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></div>\n    ";
  return buffer;
  }

  buffer += "<th class=\"subindicator\">";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</th>\n<td class=\"target\">";
  if (stack1 = helpers.baseline) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.baseline); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n<td class=\"target\">";
  if (stack1 = helpers.milestone) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.milestone); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</td>\n";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n<td class=\"subindicator-rating\">\n    <div data-subview=\"resultRating\"></div>\n</td>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-header-row"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\n<th data-subview=\"itemView\" \n    data-subview-id=\""
    + escapeExpression(((stack1 = (depth0 && depth0.id)),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\"></th>\n";
  return buffer;
  }

  buffer += "<th ></th>\n<th class=\"target\">\n    ";
  if (stack1 = helpers.baseline) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.baseline); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</th>\n<th class=\"target\">\n    ";
  if (stack1 = helpers.milestone) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.milestone); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\n</th>\n";
  stack1 = helpers.each.call(depth0, (depth0 && depth0.items), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n<td data-subview=\"itemView\" data-subview-id=\"new\"></td>\n<td class=\"\"></td>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-heading"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div data-subview=\"dateEditor\"></div>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-indicator-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<table>\n    <tbody>\n    <tr>\n        <td class=\"monitor-indicator-title\">\n            <h2 class=\"heading\">";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</h2>\n        </td>\n        <td class=\"indicator-description\" colspan=\"2\">\n            ";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </td>\n    </tr>\n    <tr>\n        <td colspan=\"3\">\n            <table class=\"monitor-subindicator-table\">\n                <thead>\n                    <tr data-subview=\"headerRow\"></tr>\n                </thead>\n                <tbody data-subview=\"subindicatorRows\"></tbody>\n            </table>\n        </td>\n    </tr>\n    </tbody>\n</table>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-result-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression;


  buffer += "<table class=\"monitor-result\">\n    <tbody>\n    <tr>\n        <td class=\"overview-title ribbon\">\n            <h2 class=\"heading\">";
  if (stack1 = helpers.name) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.name); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "</h2>\n        </td>\n        <td class=\"overview-description\">\n            ";
  if (stack1 = helpers.description) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.description); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </td>\n        <td class=\"monitor-rating\">\n            <div data-subview=\"resultRating\"></div>\n        </td>\n    </tr>\n    <tr class=\"monitor-indicator-list\">\n        <td colspan=\"3\">\n            <div data-subview=\"indicatorList\"></div>\n        </td>\n    </tr>\n</table>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["monitor-subindicator-rows"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "Hello from subindcator row template\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["overview-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<div id=\"filter-result\">\n    Lead:\n    <div data-subview=\"leadSelect\"></div>\n    <span id=\"filter-time\">\n        Start:\n        <span>\n            <input id=\"filter-time-start\" type=\"text\" placeholder=\"YYYY-MM-DD\" class=\"date addpicker\" />\n        </span>\n\n        End:\n        <span>\n            <input id=\"filter-time-end\" type=\"text\" placeholder=\"YYYY-MM-DD\" class=\"date addpicker\" />\n        </span>\n    </span>\n    <span id=\"filter-reset\">\n        <button id=\"filter-clear\" title=\"Clear filter selection\">X</button>\n    </span>\n</div>\n<div data-subview=\"resultList\"></div>\n<div data-subview=\"exportData\"></div>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["result-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  


  return "<table class=\"logframe-result\">\n    <tbody>\n        <tr>\n            <td id=\"result-detail\" class=\"tall\">\n                <div data-subview=\"resultName\"></div>\n                <div data-subview=\"resultDescription\"></div>\n                <div data-subview=\"resultContribution\"></div>\n            </td>\n            <td id=\"indicator-column\">\n                <div data-subview=\"indicatorList\"></div>\n            </td>\n            <td id=\"result-assumptions\" class=\"tall\">\n                <div class=\"ribbon ribbon-assumptions\">\n                    <h3 class=\"heading assumptions\">Assumptions</h3>\n                </div>\n                <div>\n                    <div data-subview=\"assumptionList\">No assumptions</div>\n                </div>\n                <div class=\"at-bottom\">\n                    Risk Rating:\n                    <span data-subview=\"resultRiskRating\"></span>\n                </div>\n            </td>\n        </tr>\n    </tbody>\n</table>\n";
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["result-contribution-weighting"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.contribution_weighting) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.contribution_weighting); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  
  return "0";
  }

  buffer += "Impact Weighting:\n<span data-name=\"contribution_weighting\"\n      class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.contribution_weighting), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n      >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.contribution_weighting), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</span>\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["result-overview-container"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "<span class=\"toggle-triangle";
  if (stack1 = helpers.open_toggle) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.open_toggle); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">▶</span>";
  return buffer;
  }

function program3(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "<a href=\"/design/";
  if (stack1 = helpers.log_frame) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.log_frame); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "/result/";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.id); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "/\" class=\"edit-result\">";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(6, program6, data),fn:self.program(4, program4, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</a>";
  return buffer;
  }
function program4(depth0,data) {
  
  
  return "Edit";
  }

function program6(depth0,data) {
  
  
  return "View";
  }

function program8(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "<a href=\"/monitor/";
  if (stack1 = helpers.log_frame) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.log_frame); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "/result/";
  if (stack1 = helpers.id) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.id); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "/\" class=\"monitor-result\">Monitor</a>";
  return buffer;
  }

function program10(depth0,data) {
  
  
  return "<div data-subview=\"overviewItems\"></div>";
  }

  buffer += "<table data-parent=\"";
  if (stack1 = helpers.parent) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.parent); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\" class=\"result-overview-table level-";
  if (stack1 = helpers.level) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.level); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  buffer += escapeExpression(stack1)
    + "\">\n    <tbody>\n    <tr>\n        <td class=\"overview-minmax unselectable\">";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</td>\n        <td class=\"overview-title\">\n            <div data-subview=\"resultName\"></div>\n        </td>\n        <td class=\"overview-manage\">\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n            ";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n        </td>\n        <td class=\"overview-description status-background\">\n            <div data-subview=\"resultDescription\"></div>\n        </td>\n        <td class=\"overview-rating\">\n            <div data-subview=\"resultRating\"></div>\n        </td>\n    </tr>\n    </tbody>\n</table>\n";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.id), {hash:{},inverse:self.noop,fn:self.program(10, program10, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\n";
  return buffer;
  });;
this["Aptivate"] = this["Aptivate"] || {};
this["Aptivate"]["data"] = this["Aptivate"]["data"] || {};
this["Aptivate"]["data"]["templates"] = this["Aptivate"]["data"]["templates"] || {};
this["Aptivate"]["data"]["templates"]["target-value-cell"] = Handlebars.template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [4,'>= 1.0.0'];
helpers = this.merge(helpers, Handlebars.helpers); data = data || {};
  var buffer = "", stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  
  return "editable";
  }

function program3(depth0,data) {
  
  
  return " missing";
  }

function program5(depth0,data) {
  
  var stack1;
  if (stack1 = helpers.value) { stack1 = stack1.call(depth0, {hash:{},data:data}); }
  else { stack1 = (depth0 && depth0.value); stack1 = typeof stack1 === functionType ? stack1.call(depth0, {hash:{},data:data}) : stack1; }
  return escapeExpression(stack1);
  }

function program7(depth0,data) {
  
  var stack1;
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.program(10, program10, data),fn:self.program(8, program8, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  }
function program8(depth0,data) {
  
  
  return "Click to add value";
  }

function program10(depth0,data) {
  
  
  return "&nbsp;";
  }

  buffer += "<div data-name=\"value\" \n     class=\"";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.editable), {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  stack1 = helpers.unless.call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.noop,fn:self.program(3, program3, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "\"\n     >";
  stack1 = helpers['if'].call(depth0, (depth0 && depth0.value), {hash:{},inverse:self.program(7, program7, data),fn:self.program(5, program5, data),data:data});
  if(stack1 || stack1 === 0) { buffer += stack1; }
  buffer += "</div>\n";
  return buffer;
  });;