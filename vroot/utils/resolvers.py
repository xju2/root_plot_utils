from omegaconf import OmegaConf

def add_my_resolvers():
    def resolve_if(condition, true_value, false_value):
        return true_value if condition else false_value

    OmegaConf.register_new_resolver("if", resolve_if)

    track_parameter_names = ["d0", "z0", "qoverp", "pt", "z0sin", "theta", "phi"]
    OmegaConf.register_new_resolver("ex_tp",
                                    lambda x: [x + y for y in track_parameter_names])
    OmegaConf.register_new_resolver("ex_tp_vals",
                                    lambda x: [x for _ in range(len(track_parameter_names))])

    OmegaConf.register_new_resolver("ex_ctp",
                                    lambda x, ys: [x + y.strip() for y in ys.split(",")])
    OmegaConf.register_new_resolver("gen_list",
                                    lambda x, y: [x] * y)

    OmegaConf.register_new_resolver("eval", eval)
