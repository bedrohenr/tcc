from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3

class GlobalQoSMeterApp(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(GlobalQoSMeterApp, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id

        self.logger.info(f"Switch conectado: DPID {dpid}. A injetar Meter e regra global...")

        # --- PASSO 1: Criar o Meter no Switch ---
        # Define a banda máxima (ex: 5000 kbps = 5 Mbps) com política de descarte (DROP)
        bands = [parser.OFPMeterBandDrop(rate=5000, burst_size=0)]
        
        meter_mod = parser.OFPMeterMod(
            datapath=datapath,
            command=ofproto.OFPMC_ADD,
            flags=ofproto.OFPMF_KBPS,  # Unidade em Kbps
            meter_id=1,                # ID do medidor
            bands=bands
        )
        datapath.send_msg(meter_mod)

        # --- PASSO 2: Criar a Regra de Fluxo Global (Todas as Portas) ---
        # Match vazio abrange todo o tráfego, independentemente da porta de entrada (in_port)
        match = parser.OFPMatch()
        
        # Instruções: 1º Passa pelo Meter 1, 2º Encaminha o pacote normalmente (OFPP_NORMAL)
        instructions = [
            parser.OFPInstructionMeter(1),
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            )
        ]

        # Prioridade baixa (ex: 1) para atuar como regra padrão de fallback
        flow_mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=1,
            match=match,
            instructions=instructions
        )
        datapath.send_msg(flow_mod)
        
        self.logger.info(f"Meter 1 e regra global aplicados com sucesso no switch {dpid}!")