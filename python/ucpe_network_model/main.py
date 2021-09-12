# -*- coding: utf-8 -*-
# File              : main.py
# Author            : Dmytro Shytyi
# Site              : https://dmytro.shytyi.net
# Date              : 11.09.2021
# Last Modified Date: 11.09.2021
# Last Modified By  : Dmytro Shytyi
# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service

class ServiceCallbacks(Service):

    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        
        proplist = self._dosiOsSfHandler(tctx, root, service, proplist)
        proplist = self._dosiOsSwIfHandler(tctx, root, service, proplist)
        
        matrixKeeperList = [] 
        matrixKeeperList = self._dosiOsMatrixFromLneToAllHandler(tctx, root, service, proplist, matrixKeeperList) 
        matrixKeeperList = self._dosiOsMatrixFromNiToAllHandler(tctx, root, service, proplist, matrixKeeperList) 
        matrixKeeperList = self._dosiOsMatrixFromAllToLneHandler(tctx, root, service, proplist, matrixKeeperList) 
        matrixKeeperList = self._dosiOsMatrixFromAllToNiHandler(tctx, root, service, proplist, matrixKeeperList)  
        self._matrixKeeperAnalyzer(service, matrixKeeperList)

        self._dosiOsLtHandler(tctx, root, service, proplist)
        
        return proplist
    
    class _matrixKeeper:
        def __init__(self, sf , sfPort, sfPortLink, uCpeDevice, sfType):
            self.sf = sf
            self.sfPort = sfPort
            self.sfPortLink = sfPortLink
            self.uCpeDevice = uCpeDevice
            self.sfType = sfType

    def _matrixKeeperAnalyzer(self, service, mxKpLst):
        while mxKpLst:
            mx1 = mxKpLst.pop()
            lId = mx1.sfPortLink 
            mx2 = [elem for elem in mxKpLst if elem.sfPortLink == lId]
            for el in mx2:
                mxKpLst.remove(el)
                if mx1.sfType == "ni" and el.sfType == "lne":
                    template = ncs.template.Template(service)
                    varsDosiOsMatrix = ncs.template.Variables()
                    varsDosiOsMatrix.add('dosiOS-device', mx1.uCpeDevice)
                    varsDosiOsMatrix.add('dosiOS-sw', mx1.sf)
                    varsDosiOsMatrix.add('dosiOS-port', mx1.sfPort)
                    varsDosiOsMatrix.add('dosiOS-vm', el.sf)
                    varsDosiOsMatrix.add('dosiOS-vm-port', el.sfPort)
                    template.apply('ucpe-sw-sf', varsDosiOsMatrix)

                if mx1.sfType == "lne" and el.sfType == "ni":
                    template = ncs.template.Template(service)
                    varsUcpeMatrix2 = ncs.template.Variables()
                    varsUcpeMatrix2.add('dosiOS-device', mx1.uCpeDevice)
                    varsUcpeMatrix2.add('dosiOS-sw', el.sf)
                    varsUcpeMatrix2.add('dosiOS-port', el.sf.Port)
                    varsUcpeMatrix2.add('dosiOS-vm', mx1.sf)
                    varsUcpeMatrix2.add('dosiOS-vm-port', mx1.sfPort)
                    template.apply('ucpe-sw-sf', varsUcpeMatrix2)

    def _dosiOsLtHandler(self, tctx, root, service, proplist):
        for lt in service.te.te_node_attributes.service_function.link_terminations.link_termination:
            if lt.to.service_function_id in root.network_instances.network_instance:
                template = ncs.template.Template(service)
                varsDosiOsMatrixTp = ncs.template.Variables()
                varsDosiOsMatrixTp.add('dosiOS-if',lt.tet_sf__from.tp_ref)
                varsDosiOsMatrixTp.add('dosiOS-sw',lt.tet_sf__to.service_function_id)
                varsDosiOsMatrixTp.add('dosiOS-port',lt.tet_sf__to.sf_connection_point_id)
                varsDosiOsMatrixTp.add('dosiOS-device',service.node_id)
                template.apply('ucpe-sw-if', varsDosiOsMatrixTp)

        
    def _dosiOsMatrixFromLneToAllHandler(self, tctx, root, service, proplist, matrixKeeperList):
        for matrix in service.te.te_node_attributes.service_function.\
        connectivity_matrices.connectivity_matrix:
            if matrix.tet_sf__from.service_function_id in root.logical_network_elements.logical_network_element:
                mk = self._matrixKeeper( 
                                         matrix.tet_sf__from.service_function_id,
                                         matrix.tet_sf__from.sf_connection_point_id,
                                         matrix.virtual_link_id,
                                         service.node_id,
                                         "lne")
                matrixKeeperList.append(mk) 
        return matrixKeeperList                
                

    def _dosiOsMatrixFromNiToAllHandler(self, tctx, root, service, proplist, matrixKeeperList):
        for matrix in service.te.te_node_attributes.service_function.\
                connectivity_matrices.connectivity_matrix:
                    if matrix.tet_sf__from.service_function_id in root.network_instances.network_instance:
                        mk = self._matrixKeeper( 
                                                 matrix.tet_sf__from.service_function_id,
                                                 matrix.tet_sf__from.sf_connection_point_id,
                                                 matrix.virtual_link_id,
                                                 service.node_id,
                                                 "ni")
                        matrixKeeperList.append(mk) 

        return matrixKeeperList


    def _dosiOsMatrixFromAllToLneHandler(self, tctx, root, service, proplist, matrixKeeperList):
        for matrix in service.te.te_node_attributes.service_function.\
                connectivity_matrices.connectivity_matrix:
                    if matrix.to.service_function_id in root.logical_network_elements.logical_network_element:
                        mk = self._matrixKeeper( 
                                                 matrix.to.service_function_id,
                                                 matrix.to.sf_connection_point_id,
                                                 matrix.virtual_link_id,
                                                 service.node_id,
                                                 "lne")
                        matrixKeeperList.append(mk) 

        return matrixKeeperList

    def _dosiOsMatrixFromAllToNiHandler(self, tctx, root, service, proplist, matrixKeeperList):
        for matrix in service.te.te_node_attributes.service_function.\
                connectivity_matrices.connectivity_matrix:
                    if matrix.to.service_function_id in root.network_instances.network_instance:
                        mk = self._matrixKeeper( 
                                                 matrix.to.service_function_id,
                                                 matrix.to.sf_connection_point_id,
                                                 matrix.virtual_link_id,
                                                 service.node_id,
                                                 "ni")
                        matrixKeeperList.append(mk) 

        return matrixKeeperList


    def _dosiOsSwIfHandler(self, tctx, root, service, proplist):
       for ni in root.network_instances.network_instance:
            varsUcpeNi = ncs.template.Variables()
            niProp = ni.network_instance_properties
            varsUcpeNi.add('dosiOS-device',service.node_id)
            varsUcpeNi.add('dosiOS-sw',ni.name)
            templateUcpeNi = ncs.template.Template(service)
            templateUcpeNi.apply('ucpe-sw', varsUcpeNi)
            for cpId in niProp.sf_connection_points:

                varsUcpeNiCpId = ncs.template.Variables()
                varsUcpeNiCpId.add('dosiOS-device',service.node_id)
                varsUcpeNiCpId.add('dosiOS-sw',ni.name)
                varsUcpeNiCpId.add('dosiOS-port',cpId.sf_connection_point_id)
                templateUcpeNi = ncs.template.Template(service)
                templateUcpeNi.apply('ucpe-sw-ports', varsUcpeNiCpId)
       return proplist

    def _dosiOsSfHandler(self, tctx, root, service, proplist):
        for lne in root.logical_network_elements.logical_network_element:
            varsUcpeLne = ncs.template.Variables()
            lneProp=lne.logical_network_element_properties
            LneVmId=lneProp.etsi.vnfd
            VduId=lneProp.etsi.vdu
            if LneVmId and VduId:
                VrtCmptDscrptrId=root.nfv.vnfd[LneVmId].vdu[VduId].virtual_compute_desc
                CmptDscrptr=root.nfv.vnfd[LneVmId].virtual_compute_desc[VrtCmptDscrptrId]
                VrtSwImgDscrptrId=root.nfv.vnfd[LneVmId].vdu[VduId].sw_image_desc
                SwImgDscrptr=root.nfv.vnfd[LneVmId].sw_image_desc[VrtSwImgDscrptrId]

                cpIdNum = 0
                for cpId in root.nfv.vnfd[LneVmId].ext_cpd:
                    cpIdNum = cpIdNum + 1
                varsUcpeSf = ncs.template.Variables()
                varsUcpeSf.add('dosiOS-device', lneProp.supporting_node)
                varsUcpeSf.add('dosiOS-vm',     lne.name)
                varsUcpeSf.add('dosiOS-cpu',    CmptDscrptr.virtual_cpu.num_virtual_cpu)
                varsUcpeSf.add('dosiOS-ram',    CmptDscrptr.virtual_memory.size.split(".")[0])
                varsUcpeSf.add('dosiOS-qs',     256)
                varsUcpeSf.add('dosiOS-ifn',    cpIdNum)
                varsUcpeSf.add('dosiOS-dev',    0)
                varsUcpeSf.add('dosiOS-file',   SwImgDscrptr.image)
                templateUcpeSf = ncs.template.Template(service)
                templateUcpeSf.apply('ucpe-sf', varsUcpeSf)

                for lnePort in lneProp.sf_cp_params:
                    varsUcpeSfQn = ncs.template.Variables()
                    varsUcpeSfQn.add('dosiOS-device', lneProp.supporting_node)
                    varsUcpeSfQn.add('dosiOS-vm',     lne.name)
                    if (lnePort.io_acceleration.number_of_queues):
                        varsUcpeSfQn.add('dosiOS-qn', lnePort.io_acceleration.number_of_queues)
                    else:
                        varsUcpeSfQn.add('dosiOS-qn','')
                    templateUcpeSfQn = ncs.template.Template(service)
                    templateUcpeSfQn.apply('ucpe-sf-queues', vars)

        return proplist


class Main(ncs.application.Application):
    def setup(self):
        self.log.info('Main RUNNING')
        self.register_service('ucpe-network-model-servicepoint', ServiceCallbacks)

    def teardown(self):
        self.log.info('Main FINISHED')
