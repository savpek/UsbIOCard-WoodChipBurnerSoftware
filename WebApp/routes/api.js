/*
 * Serve JSON to our AngularJS client
 */

exports.settings = function (req, res) {
    res.json({
        name: 'Bob'
    });
};
