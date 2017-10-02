/*
 * View model for OctoPrint-EXOExtras
 *
 * Author: Markus Towara
 * License: AGPLv3
 */
$(function() {
    function EXOExtrasViewModel(parameters) {
        var self = this;
        self.loginState = parameters[0];
        self.terminal = parameters[1];
        self.commandString = ko.observable("");
        self.cmdHistoryIdx=-1;
		self.raspiNet = ko.observable();
		
        self.onBeforeBinding = function() {
            self.cmdHistoryIdx=self.terminal.cmdHistory.length;
        }
		
        self.sendCommand = function() {
            console.log("Hello SendCommand " + self.commandString());            
            var splitCommands = self.commandString().split(";");     
            var len = splitCommands.length;
            for(var i=0;i<len;i++){
                self.terminal.command(splitCommands[i]);
                self.terminal.sendCommand();
            }

            self.cmdHistoryIdx = self.terminal.cmdHistory.length;
            self.commandString("");
        };
		
		self.onDataUpdaterPluginMessage = function(plugin, data) {
            self.raspiNet(_.sprintf("Raspi: %s", plugin));
        };

        self.handleKeyUp = function (d, e) {
            if (e.keyCode == 13) {
                self.sendCommand();
                return false;
            }
            return true;
        }
        self.handleKeyDown = function(d,e) {
            var keyCode = e.keyCode;
            if (keyCode == 38 || keyCode == 40) {
                if (keyCode == 38 && self.terminal.cmdHistory.length > 0 && self.cmdHistoryIdx > 0) {
                    self.cmdHistoryIdx--;
                } else if (keyCode == 40 && self.cmdHistoryIdx < self.terminal.cmdHistory.length - 1) {
                    self.cmdHistoryIdx++;
                }

                if (self.cmdHistoryIdx >= 0 && self.cmdHistoryIdx < self.terminal.cmdHistory.length) {
                    self.commandString(self.terminal.cmdHistory[self.cmdHistoryIdx]);
                }
                return false;
            }
            return true;
        };

    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        EXOExtrasViewModel,
        ["loginStateViewModel","terminalViewModel"],
        ["#gcode_bar"]
    ]);
});
