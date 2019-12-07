var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/hly', function (req, res, next) {
  // res.render('index', { title: 'Express' });
  if (!req.query.code) {
    res.json({ status: 100, msg: '请求参数缺失', data: null })
  } else {
    const code_list = require("../public/code_list")
    // console.dir(code_list)
    if (code_list.filter(c => c === req.query.code).length == 0){
      res.json({ status: 100, msg: '请求参数有误', data: null })
    }else {
      const data = require(`../public/dayline/${req.query.code}.js`)
      res.json({
        status:0,
        msg: "success",
        data
      })
    }
  }
});

router.get('/zljc', function (req, res, next) {
  // res.render('index', { title: 'Express' });
  if (!req.query.code) {
    res.json({ status: 100, msg: '请求参数缺失', data: null })
  } else {
    const code_list = require("../public/code_list")
    // console.dir(code_list)
    if (code_list.filter(c => c === req.query.code).length == 0){
      res.json({ status: 100, msg: '请求参数有误', data: null })
    }else {
      const data = require(`../public/zljc/${req.query.code}.js`)
      res.json({
        status:0,
        msg: "success",
        data
      })
    }
  }
});

module.exports = router;
