<template>
  <div>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 仓库维护
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <el-input
          placeholder="关键字搜索"
          prefix-icon="el-icon-search"
          class="input-search"
          @input="find"
          clearable
          v-model="search">
        </el-input>
        <el-button type="primary" icon="el-icon-plus" @click="handleAlter" class="alter-button">新增</el-button>
      </div>
      <el-table
        :data="tableDataNew"
        class="table"
        ref="multipleTable"
        :row-class-name="tableRowClassName"
        header-cell-class-name="table-header"
      >
        <el-table-column type="expand" >
          <template slot-scope="props">
            <el-form label-position="left" inline class="demo-table-expand">
              <el-form-item label="备注：">
                <span>{{ props.row.total_remarks }}</span>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column prop="total_iden" sortable label="仓库编码"  align="center"></el-table-column>
        <el-table-column prop="orga_name" sortable label="所属组织" :filters="total_orgaSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="total_belong_center" sortable label="所属中心" :filters="total_centerSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="total_name" sortable label="仓库名称" :filters="total_nameSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="brand_name" sortable label="所属品牌" :filters="total_brandSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="total_creator" sortable label="创建人" :filters="total_creatorSet"
                         :filter-method="filter" align="center"></el-table-column>
        <el-table-column prop="total_createDate" sortable label="创建日期" align="center"></el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.row)"
            >编辑
            </el-button>
            <el-button
              type="text"
              icon="el-icon-unlock"
              class="red"
              @click="handleStop(scope.row)"
              v-if="scope.row.total_status===1"
            >停用
            </el-button>
            <el-button
              type="text"
              icon="el-icon-lock"
              class="green"
              @click="handleStart(scope.row)"
              v-if="scope.row.total_status===0"
            >启用
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
          :page-sizes="[5, 10, 20, 50, 100, 200, 500]"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="pageTotal">
        </el-pagination>
      </div>
    </div>

    <!-- 新增弹出框 -->
    <el-dialog title="新增" :visible.sync="alterVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="form" label-width="100px"  class="form" >
          <el-row>
            <el-form-item label="所属区域"  align="left">
              <el-select v-model="form.area_name" placeholder="请选择区域"  class="option" >
                <el-option
                  v-for="item in area_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item v-if="form.area_name" label="所属组织"  align="left">
              <el-select v-model="form.orga_name" placeholder="请选择组织"  class="option" >
                <el-option
                  v-for="item in orga_options[form.area_name]"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item v-if="form.area_name" label="所属中心"  align="left">
              <el-select v-model="form.total_belong_center" placeholder="请选择中心"  class="option" clearable>
                <el-option :key="''" :label="'无'" :value="''"></el-option>
                <el-option
                  v-for="item in center_options[form.area_name]"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="仓库编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.total_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="仓库名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="form.total_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="所属品牌"  align="left">
              <el-select v-model="form.brand_name" placeholder="请选择品牌"  class="option">
                <el-option
                  v-for="item in brand_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="form.total_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="alterVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveAlter">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" :visible.sync="editVisible" width="35%" :close-on-click-modal="false">
      <div class="container">
        <el-form ref="form" :model="editform" label-width="100px"  class="form" >
          <el-row>
            <el-form-item label="仓库编码" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.total_iden" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="仓库名称" class="inputs" align="left">
              <el-col :span="10">
                <el-input v-model="editform.total_name" ></el-input>
              </el-col>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="所属品牌"  align="left">
              <el-select v-model="editform.brand_name" placeholder="请选择品牌"  class="option" >
                <el-option
                  v-for="item in brand_options"
                  :key="item"
                  :label="item"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="备注" align="left">
              <el-input type="textarea" class="textarea" v-model="editform.total_remarks"
                        placeholder="请输入200字以内的描述" :autosize="{ minRows: 2, maxRows: 6}" maxlength="200" show-word-limit></el-input>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <el-row :gutter="20" class="el-row-button-save">
        <el-col :span="1" :offset="15">
          <el-button @click="editVisible = false">取 消</el-button>
        </el-col>
        <el-col :span="1" :offset="4">
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import {getAPI, postAPI} from '../../api/api'
export default {
  name: 'test',
  data () {
    return {
      area_options: [],
      orga_options: [],
      center_options: [],
      brand_options: [],
      query: {
        pageIndex: 1,
        pageSize: 5
      },
      search: '',
      form: {
        total_name: '',
        total_remarks: '',
        total_iden: '',
        orga_name: '',
        total_belong_center: '',
        brand_name: ''
      },
      total_iden: '',
      total_nameSet: [],
      total_orgaSet: [],
      total_brandSet: [],
      total_creatorSet: [],
      total_centerSet: [],
      editform: {
        total_name: '',
        total_remarks: '',
        total_iden: '',
        brand_name: ''
      },
      tableData: [],
      tableDataNew: [],
      multipleSelection: [],
      delList: [],
      alterVisible: false,
      editVisible: false,
      pageTotal: 0
    }
  },
  created () {
    this.getData()
  },
  methods: {
    getData () {
      let _this = this
      getAPI('/base/totalWareHouses').then(function (res) {
        let n = res.data.max_iden.length
        let num = parseInt(res.data.max_iden) + 1
        _this.username = String(Array(n > ('' + num).length ? (n - ('' + num).length + 1) : 0).join(0) + num)
        console.log(_this.username)
        if (!res.data.totalWareHouses) {
          return
        }
        _this.total_nameSet = []
        _this.total_orgaSet = []
        _this.total_brandSet = []
        _this.total_creatorSet = []
        _this.total_centerSet = []
        _this.tableData = res.data.totalWareHouses
        _this.pageTotal = res.data.totalWareHouses.length
        _this.find()
        let nameset = new Set()
        let orgaset = new Set()
        let brandset = new Set()
        let centerset = new Set()
        let creatorset = new Set()
        for (let i in _this.tableData) {
          nameset.add(_this.tableData[i]['total_name'])
          orgaset.add(_this.tableData[i]['orga_name'])
          brandset.add(_this.tableData[i]['brand_name'])
          centerset.add(_this.tableData[i]['total_belong_center'])
          creatorset.add(_this.tableData[i]['total_creator'])
        }
        for (let i of nameset) {
          _this.total_nameSet.push({
            text: i,
            value: i
          })
        }
        for (let i of orgaset) {
          _this.total_orgaSet.push({
            text: i,
            value: i
          })
        }
        for (let i of centerset) {
          _this.total_centerSet.push({
            text: i,
            value: i
          })
        }
        for (let i of brandset) {
          _this.total_brandSet.push({
            text: i,
            value: i
          })
        }
        for (let i of creatorset) {
          _this.total_creatorSet.push({
            text: i,
            value: i
          })
        }
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 表格每行的class样式
    tableRowClassName ({row, rowIndex}) {
      this.pageTotal = rowIndex + 1
      if (rowIndex >= (this.query.pageIndex - 1) * this.query.pageSize && rowIndex < this.query.pageIndex * this.query.pageSize) {
        return ''
      }
      return 'tableRowDisplay'
    },
    // 表格下拉筛选
    filter (value, row, column) {
      const property = column['property']
      if (row[property] === value) {
        return true
      }
      return false
    },
    // 新增
    handleAlter () {
      this.alterVisible = true
      this.getlist()
      this.form.total_iden = this.username
    },
    // 一键清除新增表单
    clearform () {
      this.form.brand_name = ''
      this.form.orga_name = ''
      this.form.total_belong_center = ''
      this.form.total_iden = ''
      this.form.total_name = ''
      this.form.total_remarks = ''
    },
    // 停用操作
    handleStop (row) {
      this.$confirm('确定要停用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.total_status = 0
          postAPI('/base/totalWareHouseStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`停用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.total_status = 1
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`停用失败`)
            row.total_status = 1
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消停用'
          })
        })
    },
    // 查询
    find () {
      this.pageTotal = 0
      this.tableDataNew = this.tableData.filter(data => !this.search ||
          String(data.total_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.orga_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.brand_name).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.total_belong_center).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.total_remarks).toLowerCase().includes(this.search.toLowerCase()) ||
          String(data.total_creator).toLowerCase().includes(this.search.toLowerCase()))
    },
    // 启用
    handleStart (row) {
      this.$confirm('确定要启用吗？', '提示', {
        type: 'warning'
      })
        .then(() => {
          let _this = this
          row.total_status = 1
          postAPI('/base/totalWareHouseStatus', row).then(function (res) {
            if (res.data.signal === 0) {
              _this.$message.success(`启用成功`)
              _this.getData()
            } else {
              _this.$message.error(res.data.message)
              row.total_status = 0
            }
          }).catch(function (err) {
            console.log(err)
            _this.$message.error(`启用失败`)
            row.total_status = 0
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消启用'
          })
        })
    },
    // 获取列表
    getlist () {
      let _this = this
      getAPI('/base/totalWareHouseNew').then(function (res) {
        console.log(res.data)
        _this.orga_options = res.data.organizations
        _this.center_options = res.data.centers
        console.log(res.data.centers['合肥'][0])
        _this.brand_options = res.data.brands
        _this.area_options = res.data.areas
      }).catch(function (err) {
        console.log(err)
      })
    },
    // 编辑操作
    handleEdit (row) {
      this.editform.total_iden = row.total_iden
      this.editform.total_name = row.total_name
      this.editform.orga_name = row.orga_name
      this.editform.brand_name = row.brand_name
      this.editform.total_belong_center = row.total_belong_center
      this.editform.total_remarks = row.total_remarks
      this.editform.id = row.id
      this.editVisible = true
    },
    // 保存编辑
    saveEdit () {
      if (!this.editform.brand_name || !this.editform.total_name || !this.editform.total_iden) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      postAPI('/base/totalWareHouseUpdate', _this.editform).then(function (res) {
        if (res.data.signal === 0) {
          _this.editVisible = false
          _this.$message.success(`修改成功`)
          _this.getData()
          _this.clearform()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`修改失败`)
        console.log(err)
      })
    },
    // 保存新增
    saveAlter () {
      if (!this.form.brand_name || !this.form.total_name || !this.form.total_iden || !this.form.area_name || !this.form.orga_name) {
        this.$message.error(`请填写完信息`)
        return
      }
      let _this = this
      _this.form.total_status = 0
      postAPI('/base/totalWareHouseAdd', _this.form).then(function (res) {
        if (res.data.signal === 0) {
          _this.$message.success(`新增成功`)
          _this.alterVisible = false
          _this.getData()
        } else {
          _this.$message.error(res.data.message)
        }
      }).catch(function (err) {
        _this.$message.error(`新增失败`)
        console.log(err)
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.query.pageIndex = val
    },
    handleSizeChange (val) {
      this.query.pageSize = val
    }
  }
}</script>

<style>
  .tableRowDisplay {
    display: none;
  }
  .el-row-button-save {
    top: 15px;
  }
  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 100%;
  }
</style>

<style scoped>
  .handle-box {
    margin-bottom: 20px;
    position: relative;
  }

  .input-search {
    width: 50%;
  }
  .alter-button{
    position: absolute;
    right:0;
  }

  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .green {
    color: GREEN;
  }
  .inputs {
    width: 635px;
  }
</style>
