
import numpy as np
import clr



clr.AddReference("/home/cv/Desktop/yolo11 opencv/radarevent/NsrRadarSdk.dll")
from NsrRadarSdk import *
from NsrRadarSdk.NsrTypes import *





from NsrRadarSdk import *
from NsrRadarSdk.NsrTypes import *

class FormRadarManage():

        def __init__(self):
            # instance fields found by C# to Python Converter:
            self._radarSelected = None
            self._radars = None
            self._components = None
            self._bindingSource1 = None
            self._groupBox_radar_set = None
            self._button2 = None
            self._button1 = None
            self._qqTextBoxEx_radar_y3 = None
            self._qqTextBoxEx_radar_y4 = None
            self._qqTextBoxEx_radar_y2 = None
            self._qqTextBoxEx_radar_y1 = None
            self._qqTextBoxEx_radar_x4 = None
            self._qqTextBoxEx_radar_x3 = None
            self._qqTextBoxEx_radar_x2 = None
            self._qqTextBoxEx_radar_x1 = None
            self._radar_HeartTime = None
            self._label17 = None
            self._label15 = None
            self._label13 = None
            self._label11 = None
            self._label16 = None
            self._label14 = None
            self._label12 = None
            self._label10 = None
            self._label7 = None
            self._groupBox2 = None
            self._textBox7 = None
            self._textBox6 = None
            self._textBox3 = None
            self._label6 = None
            self._label3 = None
            self._textBox5 = None
            self._textBox2 = None
            self._label5 = None
            self._label2 = None
            self._textBox4 = None
            self._label4 = None
            self._textBox1 = None
            self._label1 = None
            self._dataGridView1 = None
            self._groupBoxNetSet = None
            self._button3 = None
            self._label_gateway = None
            self._text_netmask = None
            self._text_ip = None
            self._text_gateway = None
            self._labelp = None
            self._label_netmask = None
            self._RadarID = None
            self._RadarIP = None
            self._RadarPort = None
            self._RadaType = None
            self._Online = None
            self._textBox8 = None
            self._button4 = None
            self._groupBox1 = None
            self._buttonConnect = None
            self._textBox10 = None
            self._label9 = None
            self._label19 = None
            self._textBox12 = None
            self._buttonDisConnect = None

            self._InitializeComponent()

            self._dataGridView1.AutoGenerateColumns = False
            self._radars = {}
            NsrSdk.Instance.Init(9000, False)
            NsrSdk.Instance.Timeout = 3000
            try:
                NsrSdk.Instance.StartReceiveBroadcast(RadarBroadcast)
            except Exception as ex:
                MessageBox.Show(str(ex))

# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            NsrSdk.Instance.TargetDetect += FormTestRadar_TargetDetect
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            NsrSdk.Instance.RadarOnlineStateChanged += _manager_RadarConnect

            self._dataGridView1.AutoGenerateColumns = False
            self._UpdateRadars()


        def _RadarBroadcast(self, radar, info):
            if radar.Ip == "192.168.61.123" and radar.Online == False:
                try:
                    #radar.Connect()
                    pass
                except Exception:

                    pass
            if radar.Ip in self._radars.keys():
                return

            self._radars[radar.Ip] = radar

# C# TO PYTHON CONVERTER TASK: Only expression lambdas are converted by C# to Python Converter:
            #            this.BeginInvoke(new Action(() =>
            #            {
            #                UpdateRadars()
            #            }
            #            ))

        #/ <summary>
        #/ refresh the radar list
        #/ </summary>
        def _UpdateRadars(self):
            self._dataGridView1.DataSource = self._radars.values()

        def _manager_RadarConnect(self, radar, online):
# C# TO PYTHON CONVERTER TASK: Only expression lambdas are converted by C# to Python Converter:
            #            this.BeginInvoke(new Action(() =>
            #            {
            #                UpdateRadars()
            #            }
            #            ))
            pass

        #/ <summary>
        #/ format target info and append to the textbox
        #/ </summary>
        #/ <param name="radar"></param>
        def _FormTestRadar_TargetDetect(self, radar, targetList):

            sb = StringBuilder(targetList.TargetNum * 40)
            now = DateTime.Now

            for item in targetList.Targets:
                sb.AppendLine("X=\t{0:s}\t, Y=\t{1:s}\t, Time\t{2:s}".format(item.X.ToString("F2"), item.Y.ToString("F2"), str(now)))

# C# TO PYTHON CONVERTER TASK: Only expression lambdas are converted by C# to Python Converter:
            #            textBox8.Invoke(new MethodInvoker(() =>
            #                {
            #                    if (textBox8.Lines.Length > 1000)
            #                        textBox8.Clear()
            #                    textBox8.AppendText(sb.ToString())
            #                }
            #            ))


        #/ <summary>
        #/ set heart time
        #/ </summary>
        #/ <param name="sender"></param>
        #/ <param name="e"></param>
        def _button1_Click(self, sender, e):
            try:
                if self._radarSelected is None:
                    MessageBox.Show("Please select alarm radar)")
                    return
                nHeartTime = int(self._radar_HeartTime.Text)

                if nHeartTime <= 0 or nHeartTime > 60:

                    MessageBox.Show("HeartTime >0 &&HeartTime<60")
                    return
                if self._radarSelected.SetHeartTime(int(nHeartTime)):
                    self._select()
                    MessageBox.Show("Set successfully")
                else:
                    MessageBox.Show("Set failure)")
            except System.Exception as ex:
                MessageBox.Show(str(ex))
                Log.Error(str(ex))

        #/ <summary>
        #/ set filter coordinate
        #/ </summary>
        #/ <param name="sender"></param>
        #/ <param name="e"></param>
        def _button2_Click(self, sender, e):
            if self._radarSelected is None:
                MessageBox.Show("Please select alarm radar)")
                return
            pts = [PointF() for _ in range(4)]
            try:
                pts[0].X = float(self._qqTextBoxEx_radar_x1.Text)
                pts[0].Y = float(self._qqTextBoxEx_radar_y1.Text)
                pts[1].X = float(self._qqTextBoxEx_radar_x2.Text)
                pts[1].Y = float(self._qqTextBoxEx_radar_y2.Text)
                pts[2].X = float(self._qqTextBoxEx_radar_x3.Text)
                pts[2].Y = float(self._qqTextBoxEx_radar_y3.Text)
                pts[3].X = float(self._qqTextBoxEx_radar_x4.Text)
                pts[3].Y = float(self._qqTextBoxEx_radar_y4.Text)

                self._radarSelected.SetCoordinate(pts)

                self._select()
                MessageBox.Show("Set successfully")
            except System.Exception as ex:
                MessageBox.Show(str(ex))
                Log.Error(str(ex))

        #/ <summary>
        #/ change radar ip
        #/ </summary>
        #/ <param name="sender"></param>
        #/ <param name="e"></param>
        def _button3_Click(self, sender, e):
            radar = None
            try:
                if self._dataGridView1.CurrentRow is not None:
                    ip = str(self._dataGridView1.CurrentRow.Cells["RadarIP"].Value)
                    radar = self._radars[ip]
                if self._radarSelected is None:
                    MessageBox.Show("Please select alarm radar)")
                    return
                if radar is not None:
                    _ip = None
                    _netmask = None
                    _gateway = None
                    try:

                        _ip = IPAddress.Parse(self._text_ip.Text)
                        if str(_ip) == radar.Ip:
                            return
                        elif str(_ip) in self._radars.keys():
                            raise ArgumentException("radar ip exist")
                        #    CheckLocalIp(_ip)
                    except:
                        MessageBox.Show("invalid ip")
                        return
                    try:
                        _netmask = IPAddress.Parse(self._text_netmask.Text)
                    except:
                        MessageBox.Show("invalid netmask")
                        return
                    try:
                        _gateway = IPAddress.Parse(self._text_gateway.Text)
                    except:
                        MessageBox.Show("invalid gateway")
                        return
                    radar.SetIpAddress(_ip, _netmask, _gateway)

                    Thread.Sleep(1000)
                    self._bindingSource1.DataSource = self._radars.values()
                    self._UpdateRadars()
                else:

                    pass
            except System.Exception as ex:
                Log.Error(str(ex))


        def _dataGridView1_CellMouseUp(self, sender, e):
            if e.Button != NsrRadarDemo.FormRadarManage.MouseButtons.Right:
                if e.RowIndex < 0:
                    return

                self._textBox7.Clear()
                self._select()
                return

            self._dataGridView1.ClearSelection()
            hit = e
            if hit.RowIndex >= 0:
                self._dataGridView1.Rows[hit.RowIndex].Selected = True
                if hit.ColumnIndex >= 0:
                    self._dataGridView1.CurrentCell = self._dataGridView1.Rows[hit.RowIndex].Cells[hit.ColumnIndex]
                else:
                    self._dataGridView1.CurrentCell = self._dataGridView1.Rows[hit.RowIndex].Cells[0]



        #/ <summary>
        #/ query radar info
        #/ </summary>
        def _select(self):
            try:
                if self._dataGridView1.CurrentRow is not None:
                    ip = str(self._dataGridView1.CurrentRow.Cells["RadarIP"].Value)
                    radar = self._radars[ip]
                    radar.Connect()
                    self._radarSelected = radar
                    if radar is not None:
                        state = rvs_PARAM_STATUS()
                        temp_ref_state = RefObject(state)
                        if radar.GetStatus(temp_ref_state):
                            state = temp_ref_state.arg_value
                            self._textBox1.Text = "0x" + state.addr.ToString("x2")
                            self._textBox2.Text = str(state.heart.time)
                            self._textBox3.Text = str(state.bee.IsOpen)
                            self._textBox4.Text = state.radarVerInfo.FirmwareVersion
                            self._textBox5.Text = state.radarVerInfo.AlgorithmVersion
                            self._textBox6.Text = state.radarVerInfo.FpgaVersion
                            self._textBox7.Clear()
                            i = 0
                            while i < radar.PtsAlarmAreaVertices.Length:
                                self._textBox7.AppendText(i.ToString("D2"))
                                self._textBox7.AppendText(" , ")
                                self._textBox7.AppendText(str(radar.PtsAlarmAreaVertices[i]))
                                self._textBox7.AppendText("\r\n")
                                i += 1

                        else:
                            state = temp_ref_state.arg_value
                            self._textBox1.Clear()
                            self._textBox2.Clear()
                            self._textBox3.Clear()
                            self._textBox4.Clear()
                            self._textBox5.Clear()
                            self._textBox6.Clear()
                            self._textBox7.Clear()
                            MessageBox.Show("Query failure)")

            except System.Exception as ex:
                MessageBox.Show(str(ex))

        def _button4_Click(self, sender, e):
            self._textBox8.Text = ""

        def _buttonConnect_Click(self, sender, e):
            try:
                ip = IPAddress.Parse(self._textBox12.Text)
                port = int(self._textBox10.Text)

                radar = NsrSdk.Instance.CreateRadar(str(ip), port)
                radar.Connect()

                self._radars[radar.Ip] = radar
                self._UpdateRadars()
            except Exception as ex:
                MessageBox.Show(str(ex))


        def _buttonDisConnect_Click(self, sender, e):
            try:
                ip = IPAddress.Parse(self._textBox12.Text)
                port = int(self._textBox10.Text)

                if str(ip) in self._radars.keys() == False:
                    return

                radar = None

                temp_out_radar = OutObject()
                self._radars.TryRemove(str(ip), temp_out_radar)
                radar = temp_out_radar.arg_value
                if radar is not None:
                    radar.DisConnect()
                self._UpdateRadars()
            except Exception as ex:
                MessageBox.Show(str(ex))





        #/ <summary>
        #/ Required designer variable.
        #/ </summary>

        #/ <summary>
        #/ Clean up any resources being used.
        #/ </summary>
        #/ <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
# C# TO PYTHON CONVERTER TASK: Python does not allow method overloads:
        def Dispose(self, disposing):
            if disposing and (self._components is not None):
                self._components.Dispose()
            super().Dispose(disposing)

# C# TO PYTHON CONVERTER TASK: There is no preprocessor in Python:
        ##region Windows Form Designer generated code

        #/ <summary>
        #/ Required method for Designer support - do not modify
        #/ the contents of this method with the code editor.
        #/ </summary>
        def _InitializeComponent(self):
            self._components = System.ComponentModel.Container()
            self._groupBox_radar_set = System.Windows.Forms.GroupBox()
            self._button2 = System.Windows.Forms.Button()
            self._qqTextBoxEx_radar_y3 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_y4 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_y2 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_y1 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_x4 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_x3 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_x2 = System.Windows.Forms.TextBox()
            self._qqTextBoxEx_radar_x1 = System.Windows.Forms.TextBox()
            self._label17 = System.Windows.Forms.Label()
            self._label15 = System.Windows.Forms.Label()
            self._label13 = System.Windows.Forms.Label()
            self._label11 = System.Windows.Forms.Label()
            self._label16 = System.Windows.Forms.Label()
            self._label14 = System.Windows.Forms.Label()
            self._label12 = System.Windows.Forms.Label()
            self._label10 = System.Windows.Forms.Label()
            self._button1 = System.Windows.Forms.Button()
            self._radar_HeartTime = System.Windows.Forms.TextBox()
            self._label7 = System.Windows.Forms.Label()
            self._groupBox2 = System.Windows.Forms.GroupBox()
            self._textBox7 = System.Windows.Forms.TextBox()
            self._textBox6 = System.Windows.Forms.TextBox()
            self._textBox3 = System.Windows.Forms.TextBox()
            self._label6 = System.Windows.Forms.Label()
            self._label3 = System.Windows.Forms.Label()
            self._textBox5 = System.Windows.Forms.TextBox()
            self._textBox2 = System.Windows.Forms.TextBox()
            self._label5 = System.Windows.Forms.Label()
            self._label2 = System.Windows.Forms.Label()
            self._textBox4 = System.Windows.Forms.TextBox()
            self._label4 = System.Windows.Forms.Label()
            self._textBox1 = System.Windows.Forms.TextBox()
            self._label1 = System.Windows.Forms.Label()
            self._dataGridView1 = System.Windows.Forms.DataGridView()
            self._RadarID = System.Windows.Forms.DataGridViewTextBoxColumn()
            self._RadarIP = System.Windows.Forms.DataGridViewTextBoxColumn()
            self._RadarPort = System.Windows.Forms.DataGridViewTextBoxColumn()
            self._RadaType = System.Windows.Forms.DataGridViewTextBoxColumn()
            self._Online = System.Windows.Forms.DataGridViewTextBoxColumn()
            self._groupBoxNetSet = System.Windows.Forms.GroupBox()
            self._button3 = System.Windows.Forms.Button()
            self._label_gateway = System.Windows.Forms.Label()
            self._text_netmask = System.Windows.Forms.TextBox()
            self._text_ip = System.Windows.Forms.TextBox()
            self._text_gateway = System.Windows.Forms.TextBox()
            self._labelp = System.Windows.Forms.Label()
            self._label_netmask = System.Windows.Forms.Label()
            self._textBox8 = System.Windows.Forms.TextBox()
            self._button4 = System.Windows.Forms.Button()
            self._bindingSource1 = System.Windows.Forms.BindingSource(self._components)
            self._groupBox1 = System.Windows.Forms.GroupBox()
            self._buttonDisConnect = System.Windows.Forms.Button()
            self._buttonConnect = System.Windows.Forms.Button()
            self._textBox10 = System.Windows.Forms.TextBox()
            self._label9 = System.Windows.Forms.Label()
            self._label19 = System.Windows.Forms.Label()
            self._textBox12 = System.Windows.Forms.TextBox()
            self._groupBox_radar_set.SuspendLayout()
            self._groupBox2.SuspendLayout()
            ((self._dataGridView1)).BeginInit()
            self._groupBoxNetSet.SuspendLayout()
            ((self._bindingSource1)).BeginInit()
            self._groupBox1.SuspendLayout()
            self.SuspendLayout()
            # 
            # groupBox_radar_set
            # 
            self._groupBox_radar_set.Controls.Add(self._button2)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_y3)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_y4)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_y2)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_y1)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_x4)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_x3)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_x2)
            self._groupBox_radar_set.Controls.Add(self._qqTextBoxEx_radar_x1)
            self._groupBox_radar_set.Controls.Add(self._label17)
            self._groupBox_radar_set.Controls.Add(self._label15)
            self._groupBox_radar_set.Controls.Add(self._label13)
            self._groupBox_radar_set.Controls.Add(self._label11)
            self._groupBox_radar_set.Controls.Add(self._label16)
            self._groupBox_radar_set.Controls.Add(self._label14)
            self._groupBox_radar_set.Controls.Add(self._label12)
            self._groupBox_radar_set.Controls.Add(self._label10)
            self._groupBox_radar_set.ForeColor = System.Drawing.Color.White
            self._groupBox_radar_set.Location = System.Drawing.Point(2, 336)
            self._groupBox_radar_set.Name = "groupBox_radar_set"
            self._groupBox_radar_set.Size = System.Drawing.Size(369, 188)
            self._groupBox_radar_set.TabIndex = 3
            self._groupBox_radar_set.TabStop = False
            self._groupBox_radar_set.Text = "Radar filter coordinate"
            # 
            # button2
            # 
            self._button2.ForeColor = System.Drawing.Color.Black
            self._button2.Location = System.Drawing.Point(254, 136)
            self._button2.Name = "button2"
            self._button2.Size = System.Drawing.Size(97, 23)
            self._button2.TabIndex = 11
            self._button2.Text = "Set"
            self._button2.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.button2.Click += new System.EventHandler(self.button2_Click)
            # 
            # qqTextBoxEx_radar_y3
            # 
            self._qqTextBoxEx_radar_y3.Location = System.Drawing.Point(282, 70)
            self._qqTextBoxEx_radar_y3.Name = "qqTextBoxEx_radar_y3"
            self._qqTextBoxEx_radar_y3.Size = System.Drawing.Size(58, 21)
            self._qqTextBoxEx_radar_y3.TabIndex = 9
            # 
            # qqTextBoxEx_radar_y4
            # 
            self._qqTextBoxEx_radar_y4.Location = System.Drawing.Point(282, 101)
            self._qqTextBoxEx_radar_y4.Name = "qqTextBoxEx_radar_y4"
            self._qqTextBoxEx_radar_y4.Size = System.Drawing.Size(58, 21)
            self._qqTextBoxEx_radar_y4.TabIndex = 9
            # 
            # qqTextBoxEx_radar_y2
            # 
            self._qqTextBoxEx_radar_y2.Location = System.Drawing.Point(282, 43)
            self._qqTextBoxEx_radar_y2.Name = "qqTextBoxEx_radar_y2"
            self._qqTextBoxEx_radar_y2.Size = System.Drawing.Size(58, 21)
            self._qqTextBoxEx_radar_y2.TabIndex = 8
            # 
            # qqTextBoxEx_radar_y1
            # 
            self._qqTextBoxEx_radar_y1.Location = System.Drawing.Point(282, 15)
            self._qqTextBoxEx_radar_y1.Name = "qqTextBoxEx_radar_y1"
            self._qqTextBoxEx_radar_y1.Size = System.Drawing.Size(58, 21)
            self._qqTextBoxEx_radar_y1.TabIndex = 7
            # 
            # qqTextBoxEx_radar_x4
            # 
            self._qqTextBoxEx_radar_x4.Location = System.Drawing.Point(158, 101)
            self._qqTextBoxEx_radar_x4.Name = "qqTextBoxEx_radar_x4"
            self._qqTextBoxEx_radar_x4.Size = System.Drawing.Size(63, 21)
            self._qqTextBoxEx_radar_x4.TabIndex = 6
            # 
            # qqTextBoxEx_radar_x3
            # 
            self._qqTextBoxEx_radar_x3.Location = System.Drawing.Point(158, 70)
            self._qqTextBoxEx_radar_x3.Name = "qqTextBoxEx_radar_x3"
            self._qqTextBoxEx_radar_x3.Size = System.Drawing.Size(63, 21)
            self._qqTextBoxEx_radar_x3.TabIndex = 5
            # 
            # qqTextBoxEx_radar_x2
            # 
            self._qqTextBoxEx_radar_x2.Location = System.Drawing.Point(158, 43)
            self._qqTextBoxEx_radar_x2.Name = "qqTextBoxEx_radar_x2"
            self._qqTextBoxEx_radar_x2.Size = System.Drawing.Size(63, 21)
            self._qqTextBoxEx_radar_x2.TabIndex = 4
            # 
            # qqTextBoxEx_radar_x1
            # 
            self._qqTextBoxEx_radar_x1.Location = System.Drawing.Point(158, 15)
            self._qqTextBoxEx_radar_x1.Name = "qqTextBoxEx_radar_x1"
            self._qqTextBoxEx_radar_x1.Size = System.Drawing.Size(63, 21)
            self._qqTextBoxEx_radar_x1.TabIndex = 3
            # 
            # label17
            # 
            self._label17.AutoSize = True
            self._label17.Font = System.Drawing.Font("宋体", 12)
            self._label17.Location = System.Drawing.Point(230, 106)
            self._label17.Name = "label17"
            self._label17.Size = System.Drawing.Size(16, 16)
            self._label17.TabIndex = 0
            self._label17.Text = "Y"
            # 
            # label15
            # 
            self._label15.AutoSize = True
            self._label15.Font = System.Drawing.Font("宋体", 12)
            self._label15.Location = System.Drawing.Point(230, 75)
            self._label15.Name = "label15"
            self._label15.Size = System.Drawing.Size(16, 16)
            self._label15.TabIndex = 0
            self._label15.Text = "Y"
            # 
            # label13
            # 
            self._label13.AutoSize = True
            self._label13.Font = System.Drawing.Font("宋体", 12)
            self._label13.Location = System.Drawing.Point(230, 48)
            self._label13.Name = "label13"
            self._label13.Size = System.Drawing.Size(16, 16)
            self._label13.TabIndex = 0
            self._label13.Text = "Y"
            # 
            # label11
            # 
            self._label11.AutoSize = True
            self._label11.Font = System.Drawing.Font("宋体", 12)
            self._label11.Location = System.Drawing.Point(230, 20)
            self._label11.Name = "label11"
            self._label11.Size = System.Drawing.Size(16, 16)
            self._label11.TabIndex = 0
            self._label11.Text = "Y"
            # 
            # label16
            # 
            self._label16.AutoSize = True
            self._label16.Font = System.Drawing.Font("宋体", 12)
            self._label16.Location = System.Drawing.Point(16, 106)
            self._label16.Name = "label16"
            self._label16.Size = System.Drawing.Size(104, 16)
            self._label16.TabIndex = 0
            self._label16.Text = "Point D    X"
            # 
            # label14
            # 
            self._label14.AutoSize = True
            self._label14.Font = System.Drawing.Font("宋体", 12)
            self._label14.Location = System.Drawing.Point(16, 75)
            self._label14.Name = "label14"
            self._label14.Size = System.Drawing.Size(104, 16)
            self._label14.TabIndex = 0
            self._label14.Text = "Point C    X"
            # 
            # label12
            # 
            self._label12.AutoSize = True
            self._label12.Font = System.Drawing.Font("宋体", 12)
            self._label12.Location = System.Drawing.Point(16, 48)
            self._label12.Name = "label12"
            self._label12.Size = System.Drawing.Size(104, 16)
            self._label12.TabIndex = 0
            self._label12.Text = "Point B    X"
            # 
            # label10
            # 
            self._label10.AutoSize = True
            self._label10.Font = System.Drawing.Font("宋体", 12)
            self._label10.Location = System.Drawing.Point(16, 20)
            self._label10.Name = "label10"
            self._label10.Size = System.Drawing.Size(104, 16)
            self._label10.TabIndex = 0
            self._label10.Text = "Point A    X"
            # 
            # button1
            # 
            self._button1.ForeColor = System.Drawing.Color.Black
            self._button1.Location = System.Drawing.Point(233, 23)
            self._button1.Name = "button1"
            self._button1.Size = System.Drawing.Size(74, 23)
            self._button1.TabIndex = 10
            self._button1.Text = "set"
            self._button1.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.button1.Click += new System.EventHandler(self.button1_Click)
            # 
            # radar_HeartTime
            # 
            self._radar_HeartTime.Location = System.Drawing.Point(95, 23)
            self._radar_HeartTime.Name = "radar_HeartTime"
            self._radar_HeartTime.Size = System.Drawing.Size(132, 21)
            self._radar_HeartTime.TabIndex = 2
            # 
            # label7
            # 
            self._label7.AutoSize = True
            self._label7.Location = System.Drawing.Point(6, 26)
            self._label7.Name = "label7"
            self._label7.Size = System.Drawing.Size(83, 12)
            self._label7.TabIndex = 0
            self._label7.Text = "heart(1-60)："
            # 
            # groupBox2
            # 
            self._groupBox2.Anchor = (((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)))
            self._groupBox2.Controls.Add(self._textBox7)
            self._groupBox2.Controls.Add(self._textBox6)
            self._groupBox2.Controls.Add(self._textBox3)
            self._groupBox2.Controls.Add(self._label6)
            self._groupBox2.Controls.Add(self._label3)
            self._groupBox2.Controls.Add(self._textBox5)
            self._groupBox2.Controls.Add(self._textBox2)
            self._groupBox2.Controls.Add(self._label5)
            self._groupBox2.Controls.Add(self._label2)
            self._groupBox2.Controls.Add(self._textBox4)
            self._groupBox2.Controls.Add(self._label4)
            self._groupBox2.Controls.Add(self._textBox1)
            self._groupBox2.Controls.Add(self._label1)
            self._groupBox2.ForeColor = System.Drawing.Color.White
            self._groupBox2.Location = System.Drawing.Point(703, 338)
            self._groupBox2.Name = "groupBox2"
            self._groupBox2.Size = System.Drawing.Size(357, 188)
            self._groupBox2.TabIndex = 4
            self._groupBox2.TabStop = False
            self._groupBox2.Text = "Radar info"
            # 
            # textBox7
            # 
            self._textBox7.Location = System.Drawing.Point(8, 107)
            self._textBox7.Multiline = True
            self._textBox7.Name = "textBox7"
            self._textBox7.Size = System.Drawing.Size(335, 75)
            self._textBox7.TabIndex = 8
            # 
            # textBox6
            # 
            self._textBox6.Enabled = False
            self._textBox6.Location = System.Drawing.Point(243, 80)
            self._textBox6.Name = "textBox6"
            self._textBox6.Size = System.Drawing.Size(100, 21)
            self._textBox6.TabIndex = 7
            # 
            # textBox3
            # 
            self._textBox3.Enabled = False
            self._textBox3.Location = System.Drawing.Point(65, 80)
            self._textBox3.Name = "textBox3"
            self._textBox3.Size = System.Drawing.Size(100, 21)
            self._textBox3.TabIndex = 6
            # 
            # label6
            # 
            self._label6.AutoSize = True
            self._label6.Location = System.Drawing.Point(184, 83)
            self._label6.Name = "label6"
            self._label6.Size = System.Drawing.Size(29, 12)
            self._label6.TabIndex = 0
            self._label6.Text = "FPGA"
            # 
            # label3
            # 
            self._label3.AutoSize = True
            self._label3.Location = System.Drawing.Point(6, 83)
            self._label3.Name = "label3"
            self._label3.Size = System.Drawing.Size(41, 12)
            self._label3.TabIndex = 0
            self._label3.Text = "Buzzer"
            # 
            # textBox5
            # 
            self._textBox5.Enabled = False
            self._textBox5.Location = System.Drawing.Point(243, 53)
            self._textBox5.Name = "textBox5"
            self._textBox5.Size = System.Drawing.Size(100, 21)
            self._textBox5.TabIndex = 5
            # 
            # textBox2
            # 
            self._textBox2.Enabled = False
            self._textBox2.Location = System.Drawing.Point(65, 53)
            self._textBox2.Name = "textBox2"
            self._textBox2.Size = System.Drawing.Size(100, 21)
            self._textBox2.TabIndex = 4
            # 
            # label5
            # 
            self._label5.AutoSize = True
            self._label5.Location = System.Drawing.Point(184, 56)
            self._label5.Name = "label5"
            self._label5.Size = System.Drawing.Size(59, 12)
            self._label5.TabIndex = 0
            self._label5.Text = "Algorithm"
            # 
            # label2
            # 
            self._label2.AutoSize = True
            self._label2.Location = System.Drawing.Point(6, 56)
            self._label2.Name = "label2"
            self._label2.Size = System.Drawing.Size(35, 12)
            self._label2.TabIndex = 0
            self._label2.Text = "Heart"
            # 
            # textBox4
            # 
            self._textBox4.Enabled = False
            self._textBox4.Location = System.Drawing.Point(243, 26)
            self._textBox4.Name = "textBox4"
            self._textBox4.Size = System.Drawing.Size(100, 21)
            self._textBox4.TabIndex = 3
            # 
            # label4
            # 
            self._label4.AutoSize = True
            self._label4.Location = System.Drawing.Point(184, 29)
            self._label4.Name = "label4"
            self._label4.Size = System.Drawing.Size(53, 12)
            self._label4.TabIndex = 0
            self._label4.Text = "Firmware"
            # 
            # textBox1
            # 
            self._textBox1.Enabled = False
            self._textBox1.Location = System.Drawing.Point(65, 26)
            self._textBox1.Name = "textBox1"
            self._textBox1.Size = System.Drawing.Size(100, 21)
            self._textBox1.TabIndex = 2
            # 
            # label1
            # 
            self._label1.AutoSize = True
            self._label1.Location = System.Drawing.Point(6, 29)
            self._label1.Name = "label1"
            self._label1.Size = System.Drawing.Size(53, 12)
            self._label1.TabIndex = 0
            self._label1.Text = "Dev addr"
            # 
            # dataGridView1
            # 
            self._dataGridView1.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize
            self._dataGridView1.Columns.AddRange([self._RadarID, self._RadarIP, self._RadarPort, self._RadaType, self._Online])
            self._dataGridView1.Location = System.Drawing.Point(2, 7)
            self._dataGridView1.Name = "dataGridView1"
            self._dataGridView1.RowTemplate.Height = 23
            self._dataGridView1.Size = System.Drawing.Size(539, 307)
            self._dataGridView1.TabIndex = 5
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.dataGridView1.CellMouseUp += new System.Windows.Forms.DataGridViewCellMouseEventHandler(self.dataGridView1_CellMouseUp)
            # 
            # RadarID
            # 
            self._RadarID.DataPropertyName = "ID"
            self._RadarID.HeaderText = "ID"
            self._RadarID.Name = "RadarID"
            self._RadarID.ReadOnly = True
            # 
            # RadarIP
            # 
            self._RadarIP.DataPropertyName = "IP"
            self._RadarIP.HeaderText = "IP"
            self._RadarIP.Name = "RadarIP"
            # 
            # RadarPort
            # 
            self._RadarPort.DataPropertyName = "Port"
            self._RadarPort.HeaderText = "Port"
            self._RadarPort.Name = "RadarPort"
            # 
            # RadaType
            # 
            self._RadaType.DataPropertyName = "Type"
            self._RadaType.HeaderText = "Type"
            self._RadaType.Name = "RadaType"
            self._RadaType.ReadOnly = True
            # 
            # Online
            # 
            self._Online.DataPropertyName = "Online"
            self._Online.HeaderText = "Online"
            self._Online.Name = "Online"
            # 
            # groupBoxNetSet
            # 
            self._groupBoxNetSet.Controls.Add(self._button3)
            self._groupBoxNetSet.Controls.Add(self._button1)
            self._groupBoxNetSet.Controls.Add(self._label_gateway)
            self._groupBoxNetSet.Controls.Add(self._text_netmask)
            self._groupBoxNetSet.Controls.Add(self._text_ip)
            self._groupBoxNetSet.Controls.Add(self._text_gateway)
            self._groupBoxNetSet.Controls.Add(self._labelp)
            self._groupBoxNetSet.Controls.Add(self._label_netmask)
            self._groupBoxNetSet.Controls.Add(self._label7)
            self._groupBoxNetSet.Controls.Add(self._radar_HeartTime)
            self._groupBoxNetSet.ForeColor = System.Drawing.Color.White
            self._groupBoxNetSet.Location = System.Drawing.Point(377, 336)
            self._groupBoxNetSet.Name = "groupBoxNetSet"
            self._groupBoxNetSet.Size = System.Drawing.Size(320, 188)
            self._groupBoxNetSet.TabIndex = 14
            self._groupBoxNetSet.TabStop = False
            self._groupBoxNetSet.Text = "Radar params set"
            # 
            # button3
            # 
            self._button3.ForeColor = System.Drawing.Color.Black
            self._button3.Location = System.Drawing.Point(232, 134)
            self._button3.Name = "button3"
            self._button3.Size = System.Drawing.Size(75, 25)
            self._button3.TabIndex = 35
            self._button3.Text = "change ip"
            self._button3.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.button3.Click += new System.EventHandler(self.button3_Click)
            # 
            # label_gateway
            # 
            self._label_gateway.AutoSize = True
            self._label_gateway.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (int((134))))
            self._label_gateway.Location = System.Drawing.Point(7, 139)
            self._label_gateway.Name = "label_gateway"
            self._label_gateway.Size = System.Drawing.Size(56, 17)
            self._label_gateway.TabIndex = 32
            self._label_gateway.Text = "gateway"
            # 
            # text_netmask
            # 
            self._text_netmask.Location = System.Drawing.Point(95, 97)
            self._text_netmask.MinimumSize = System.Drawing.Size(20, 24)
            self._text_netmask.Name = "text_netmask"
            self._text_netmask.Size = System.Drawing.Size(131, 24)
            self._text_netmask.TabIndex = 31
            # 
            # text_ip
            # 
            self._text_ip.Location = System.Drawing.Point(95, 59)
            self._text_ip.MinimumSize = System.Drawing.Size(20, 24)
            self._text_ip.Name = "text_ip"
            self._text_ip.Size = System.Drawing.Size(131, 24)
            self._text_ip.TabIndex = 28
            # 
            # text_gateway
            # 
            self._text_gateway.Location = System.Drawing.Point(95, 135)
            self._text_gateway.MinimumSize = System.Drawing.Size(20, 24)
            self._text_gateway.Name = "text_gateway"
            self._text_gateway.Size = System.Drawing.Size(131, 24)
            self._text_gateway.TabIndex = 33
            # 
            # labelp
            # 
            self._labelp.AutoSize = True
            self._labelp.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (int((134))))
            self._labelp.Location = System.Drawing.Point(7, 63)
            self._labelp.Name = "labelp"
            self._labelp.Size = System.Drawing.Size(19, 17)
            self._labelp.TabIndex = 27
            self._labelp.Text = "ip"
            # 
            # label_netmask
            # 
            self._label_netmask.AutoSize = True
            self._label_netmask.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (int((134))))
            self._label_netmask.Location = System.Drawing.Point(7, 101)
            self._label_netmask.Name = "label_netmask"
            self._label_netmask.Size = System.Drawing.Size(57, 17)
            self._label_netmask.TabIndex = 30
            self._label_netmask.Text = "netmask"
            # 
            # textBox8
            # 
            self._textBox8.Location = System.Drawing.Point(547, 7)
            self._textBox8.Multiline = True
            self._textBox8.Name = "textBox8"
            self._textBox8.ScrollBars = System.Windows.Forms.ScrollBars.Vertical
            self._textBox8.Size = System.Drawing.Size(756, 304)
            self._textBox8.TabIndex = 15
            # 
            # button4
            # 
            self._button4.ForeColor = System.Drawing.Color.Black
            self._button4.Location = System.Drawing.Point(946, 317)
            self._button4.Name = "button4"
            self._button4.Size = System.Drawing.Size(100, 23)
            self._button4.TabIndex = 16
            self._button4.Text = "Clear targets"
            self._button4.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.button4.Click += new System.EventHandler(self.button4_Click)
            # 
            # bindingSource1
            # 
            self._bindingSource1.DataSource = typeof(NsrRadarSdk.NsrRadar)
            # 
            # groupBox1
            # 
            self._groupBox1.Controls.Add(self._buttonDisConnect)
            self._groupBox1.Controls.Add(self._buttonConnect)
            self._groupBox1.Controls.Add(self._textBox10)
            self._groupBox1.Controls.Add(self._label9)
            self._groupBox1.Controls.Add(self._label19)
            self._groupBox1.Controls.Add(self._textBox12)
            self._groupBox1.ForeColor = System.Drawing.Color.White
            self._groupBox1.Location = System.Drawing.Point(1066, 338)
            self._groupBox1.Name = "groupBox1"
            self._groupBox1.Size = System.Drawing.Size(240, 188)
            self._groupBox1.TabIndex = 14
            self._groupBox1.TabStop = False
            self._groupBox1.Text = "Manual connect"
            # 
            # buttonDisConnect
            # 
            self._buttonDisConnect.ForeColor = System.Drawing.Color.Black
            self._buttonDisConnect.Location = System.Drawing.Point(85, 126)
            self._buttonDisConnect.Name = "buttonDisConnect"
            self._buttonDisConnect.Size = System.Drawing.Size(74, 23)
            self._buttonDisConnect.TabIndex = 10
            self._buttonDisConnect.Text = "Disconnect"
            self._buttonDisConnect.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.buttonDisConnect.Click += new System.EventHandler(self.buttonDisConnect_Click)
            # 
            # buttonConnect
            # 
            self._buttonConnect.ForeColor = System.Drawing.Color.Black
            self._buttonConnect.Location = System.Drawing.Point(85, 97)
            self._buttonConnect.Name = "buttonConnect"
            self._buttonConnect.Size = System.Drawing.Size(74, 23)
            self._buttonConnect.TabIndex = 10
            self._buttonConnect.Text = "Connect"
            self._buttonConnect.UseVisualStyleBackColor = True
# C# TO PYTHON CONVERTER TASK: Python has no equivalent to C#-style event wireups:
            self.buttonConnect.Click += new System.EventHandler(self.buttonConnect_Click)
            # 
            # textBox10
            # 
            self._textBox10.Location = System.Drawing.Point(85, 59)
            self._textBox10.MinimumSize = System.Drawing.Size(20, 24)
            self._textBox10.Name = "textBox10"
            self._textBox10.Size = System.Drawing.Size(141, 21)
            self._textBox10.TabIndex = 28
            # 
            # label9
            # 
            self._label9.AutoSize = True
            self._label9.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, (int((134))))
            self._label9.Location = System.Drawing.Point(7, 63)
            self._label9.Name = "label9"
            self._label9.Size = System.Drawing.Size(33, 17)
            self._label9.TabIndex = 27
            self._label9.Text = "port"
            # 
            # label19
            # 
            self._label19.AutoSize = True
            self._label19.Location = System.Drawing.Point(6, 26)
            self._label19.Name = "label19"
            self._label19.Size = System.Drawing.Size(17, 12)
            self._label19.TabIndex = 0
            self._label19.Text = "ip"
            # 
            # textBox12
            # 
            self._textBox12.Location = System.Drawing.Point(85, 23)
            self._textBox12.Name = "textBox12"
            self._textBox12.Size = System.Drawing.Size(142, 21)
            self._textBox12.TabIndex = 2
            self._textBox12.Text = "192.168.61.123"
            # 
            # FormRadarManage
            # 
            self.AutoScaleDimensions = System.Drawing.SizeF(6, 12)
            self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
            self.BackColor = System.Drawing.Color.FromArgb((int(((int((0)))))), (int(((int((139)))))), (int(((int((69)))))))
            self.ClientSize = System.Drawing.Size(1315, 536)
            self.Controls.Add(self._button4)
            self.Controls.Add(self._textBox8)
            self.Controls.Add(self._groupBox1)
            self.Controls.Add(self._groupBoxNetSet)
            self.Controls.Add(self._dataGridView1)
            self.Controls.Add(self._groupBox_radar_set)
            self.Controls.Add(self._groupBox2)
            self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow
            self.Name = "FormRadarManage"
            self.Text = "FormRadarManage"
            self._groupBox_radar_set.ResumeLayout(False)
            self._groupBox_radar_set.PerformLayout()
            self._groupBox2.ResumeLayout(False)
            self._groupBox2.PerformLayout()
            ((self._dataGridView1)).EndInit()
            self._groupBoxNetSet.ResumeLayout(False)
            self._groupBoxNetSet.PerformLayout()
            ((self._bindingSource1)).EndInit()
            self._groupBox1.ResumeLayout(False)
            self._groupBox1.PerformLayout()
            self.ResumeLayout(False)
            self.PerformLayout()


# C# TO PYTHON CONVERTER TASK: There is no preprocessor in Python:
        ##endregion