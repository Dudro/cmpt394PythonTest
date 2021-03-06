"""
A module to collect statistical information about
values of population for a surface.  By calling
the get_stats method a dictionary full of these
values is returned.
This module also contains functionality for producing
scatter plots with this data from module plotly.
"""
import Surface
import Cell as c
import Gene as g
import statistics as s

def init_move_stats(surface, stats):
    """
    Create the keys 'init_move_frac' in the
    'stats' dictionary and populate it with
    data about the default choice of the surface's
    population.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
    # get initial move statistics
    if 0 != surface.population:
        initial_moves = list()
        surface.my_map(
            lambda c: initial_moves.append(
                c.get_gene().get_choice_at(1)))
    
        init_move_frac = 0
        for move in initial_moves:
            if 'd' is move:
                init_move_frac += 1
        init_move_frac = float(init_move_frac)/len(initial_moves)
        
        stats['init_move_frac'] = init_move_frac * 100.0
    else:
        stats['init_move_frac'] = None

def fraction_def_stats(surface, stats):
    """
    Create the keys 'def_frac_mean' and 'def_frac_stddev' in the
    'stats' dictionary and populate it with data about the 
    fraction of Cell's Gene's which are 'd'.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
   # get gene defection fraction stats
    if 0 != surface.population:
        fraction_defect = list()

        surface.my_map(
                lambda c: fraction_defect.append(
                    c.get_gene().get_defect_fraction()))
        mean = s.mean(fraction_defect)
        stddev = s.pstdev(fraction_defect, mean)
    else:
        mean = 0
        stddev = 0

    stats['def_frac_mean'] = mean * 100.0
    stats['def_frac_stddev'] = stddev * 100.0

def gene_length_stats(surface, stats):
    """
    Create the keys 'length_mean' and 'length_stddev' in the
    'stats' dictionary and populate it with data about the 
    length of the surface's Cells' Genes.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """

    if 0 != surface.population:
        lengths = list()
        surface.my_map(lambda c: lengths.append(len(c.get_gene().get_seq())-1))
        mean = s.mean(lengths)
        stddev = s.pstdev(lengths, mean)
    else:
        mean = None
        stddev = None

    stats['length_mean'] = mean
    stats['length_stddev'] = stddev

def get_score_stats(surface, stats):
    """
    Create the keys 'scores_mean' and 'scores_stddev' in the
    'stats' dictionary and populate it with data about the 
    scores of the surface's Cells.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
    if 0 != surface.population:
        scores = list()
        surface.my_map(lambda c: scores.append(c.get_score()))
        mean = s.mean(scores)
        stddev = s.pstdev(scores, mean)
    else:
        mean = None
        stddev = None

    stats['scores_mean'] = mean
    stats['scores_stddev'] = stddev

def get_age_stats(surface, stats):
    """
    Create the keys 'age_mean' and 'age_stddev' in the
    'stats' dictionary and populate it with data about the 
    ages of the surface's Cells.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
    if 0 != surface.population:
        ages = list()
        surface.my_map(lambda c: ages.append(c.get_age()))
        mean = s.mean(ages)
        stddev = s.pstdev(ages, mean)
    else:
        mean = None
        stddev = None

    stats['age_mean'] = mean
    stats['age_stddev'] = stddev

def get_rule_stats(surface, stats):
    """
    Create the keys:
        'rule_frac_tfts'
        'rule_frac_t2ts'
        'rule_frac_ftfs'
        'rule_frac_alld'
        'rule_frac_allc'
    in the 'stats' dictionary and populate it with data about the 
    fraction of the surface's population which are specific rules.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
    if 0 != surface.population:
        num_tfts = 0
        num_t2ts = 0
        num_ftfs = 0
        num_alld = 0
        num_allc = 0
        for c in surface.get_all():
            if c.is_tft():
                num_tfts += 1
            elif c.is_t2t():
                num_t2ts += 1
            elif c.is_ftf():
                num_ftfs += 1
            elif c.is_alld():
                num_alld += 1
            elif c.is_allc():
                num_allc += 1
        frac_tfts = float(num_tfts)/surface.population
        frac_t2ts = float(num_t2ts)/surface.population
        frac_ftfs = float(num_ftfs)/surface.population
        frac_alld = float(num_alld)/surface.population
        frac_allc = float(num_allc)/surface.population
    else:
        frac_tfts = 0
        frac_t2ts = 0
        frac_ftfs = 0
        frac_alld = 0
        frac_allc = 0

    stats['rule_frac_tfts'] = frac_tfts * 100.0
    stats['rule_frac_t2ts'] = frac_t2ts * 100.0
    stats['rule_frac_ftfs'] = frac_ftfs * 100.0
    stats['rule_frac_alld'] = frac_alld * 100.0
    stats['rule_frac_allc'] = frac_allc * 100.0

def get_population_stats(surface, stats):
    """
    Create the keys 'pop_rel' and 'pop_abs' in the
    'stats' dictionary and populate it with data about the 
    relative and absolute population of the surface.
    :param surface: The surface from which to collect data
    :type surface: Surface
    :param stats: The dictionary into which the data should be inserted
    :type stats: dict(str,float)
    """
    map_size = surface.width * surface.height
    rel_population = float(surface.population) / float(map_size)
    stats['pop_rel'] = rel_population * 100.0
    stats['pop_abs'] = surface.population
    

def get_stats(surface):
    """
    Retrieve statistics about the Surface and the
    Cellular population.
    :param surface: The surface of a simulation
    :type surface: Surface
    :return: A dictionary full of statistics
    :rtype: dict(str, float)
    """
    stats = dict()
   
    init_move_stats(surface, stats)
    fraction_def_stats(surface, stats)
    gene_length_stats(surface, stats)
    get_score_stats(surface, stats)
    get_rule_stats(surface, stats)
    get_age_stats(surface, stats)

    return stats
    
def output_plot(path, data):
    from plotly import offline as py
    from plotly import graph_objs as go

    plot_data = {}
    for key in data[0].keys():
        plot_data[key] = {
            'x': [],
            'y': [],
            'mode': 'lines+markers',
            'name': key
        }

    for i, d in enumerate(data):
        for k, v in d.items():
            plot_data[k]['x'].append(i)
            plot_data[k]['y'].append(v)

    to_plot = []
    for k in sorted(plot_data.keys()):
        to_plot.append(go.Scatter(plot_data[k]))

    py.plot(to_plot, filename=path, auto_open=False)

